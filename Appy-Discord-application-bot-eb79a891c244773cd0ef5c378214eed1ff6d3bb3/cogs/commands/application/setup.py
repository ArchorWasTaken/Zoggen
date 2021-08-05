import asyncio

from discord.ext import commands
from helpers import embedHelper


class Setup(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        description="Provides a list of the bots commands.",
        aliases=["createapplication"],
    )
    @commands.has_permissions(manage_guild=True)
    async def setup(self, ctx):
        embed = await embedHelper.default_embed(self.client, "Application setup")
        embed.description = (
            "```ini\n[Welcome to the interactive setup command. I will walk you through making your "
            "application!]``````fix\nAre you sure you wan't to start the application process?```"
            "\n**Please respond with `yes` or `no`**"
        )
        await ctx.channel.send(embed=embed)
        try:
            while True:
                msg = await self.client.wait_for(
                    "message",
                    check=lambda message: message.author == ctx.author
                    and message.channel.id == ctx.channel.id,  # noqa W503
                    timeout=60,
                )
                if msg.content.lower() == "yes":
                    return await self.start_setup(ctx)

                elif msg.content.lower() == "no":
                    embed = await embedHelper.error_embed(
                        self.client, "Application setup"
                    )
                    embed.description = (
                        "You just canceled the application process.\nMade a mistake? "
                        "Run the `!setup` command again!"
                    )
                    return await ctx.channel.send(embed=embed)
                else:
                    embed.description = "That is not a valid response. Please respond with `yes` or `no`"
                    await ctx.channel.send(embed=embed)
        except asyncio.TimeoutError:
            embed = await embedHelper.error_embed(self.client, "Application setup")
            embed.description = (
                "```diff\n- Application canceled. You took to long to respond.```"
            )
            await ctx.channel.send(embed=embed)
            return

    async def start_setup(self, ctx):
        application_name = ""
        log_channel = 0
        embed = await embedHelper.default_embed(self.client, "Application setup")
        embed.description = (
            "```ini\n[What is the name of your application?]```\n**The name is how users will "
            "apply for the application.**"
        )
        await ctx.send(embed=embed)
        try:
            while True:
                msg = await self.client.wait_for(
                    "message",
                    check=lambda message: message.author == ctx.author
                    and message.channel.id == ctx.channel.id,  # noqa W503
                    timeout=800,
                )
                if msg.content.lower() == "cancel":
                    embed.description = "The application has been canceled."
                    return await ctx.channel.send(embed=embed)
                check_for_duplicate_appname = await self.client.applications.find_one(
                    {"name": msg.content.lower(), "guildId": ctx.guild.id}
                )
                if check_for_duplicate_appname:
                    embed = await embedHelper.error_embed(
                        self.client, "This name has already been used."
                    )
                    embed.description = (
                        "```diff\n- There is already an application with this name. "
                        "\n\nPlease respond with a different name.```"
                    )
                    await ctx.channel.send(embed=embed)
                else:
                    break
            application_name = msg.content.lower()
            embed = await embedHelper.default_embed(self.client, "Application setup")
            embed.description = "```ini\n[Please mention the channel where you want your application logs to be sent.]```"
            await ctx.send(embed=embed)
            while True:
                msg = await self.client.wait_for(
                    "message",
                    check=lambda message: message.author == ctx.author
                    and message.channel.id == ctx.channel.id,  # noqa W503
                    timeout=800,
                )
                if msg.content.lower() == "cancel":
                    embed = await embedHelper.error_embed(
                        self.client, "Application canceled"
                    )
                    embed.description = "The application has been canceled"
                    return await ctx.channel.send(embed=embed)
                if not msg.channel_mentions:
                    embed = await embedHelper.error_embed(
                        self.client, "Incorrect value"
                    )
                    embed.description = (
                        "```diff\n-Incorrect channel. Please mention a channel to proceed to the next question.```"
                        f"\n`Example:` <#{ctx.channel.id}>"
                    )
                    await ctx.send(embed=embed)
                else:
                    log_channel = msg.channel_mentions[0].id
                    break
            questions = []
            maximum_questions = 24
            for question in range(maximum_questions):
                embed = await embedHelper.default_embed(
                    self.client, f"Question {question + 1}"
                )
                embed.set_thumbnail(url=self.client.user.avatar_url)
                embed.description = (
                    f"Please enter a value for **Question {question + 1}**.\n\nType `Cancel` to "
                    "cancel your application, or `Done` to end the application process."
                )
                await ctx.send(embed=embed)
                msg = await self.client.wait_for(
                    "message",
                    check=lambda message: message.author == ctx.author
                    and message.channel.id == ctx.channel.id,  # noqa W503
                    timeout=180,
                )
                if msg.content.lower() == "cancel":
                    embed.description = "The application has been canceled."
                    return await ctx.channel.send(embed=embed)
                if msg.content.lower() != "done":
                    questions.append(msg.content)
                if msg.content.lower() == "done":
                    new_application = {
                        "name": application_name,
                        "guildId": ctx.guild.id,
                        "application_creator": ctx.author.id,
                        "log_channel": log_channel,
                        "enabled": True,
                        "questions": questions,
                    }
                    if len(questions) == 0:
                        embed = await embedHelper.error_embed(
                            self.client, "No questions were given."
                        )
                        embed.description = (
                            "```diff\n- Your application was not created. "
                            "This was due to a lack of questions given.```"
                        )
                        return await ctx.channel.send(embed=embed)
                    self.client.applications.insert_one(new_application)
                    embed = await embedHelper.success_embed(
                        self.client, "Application form created."
                    )
                    embed.description = (
                        f"{application_name} application has been created successfully."
                    )
                    return await ctx.channel.send(embed=embed)
            new_application = {
                "name": application_name,
                "guildId": ctx.guild.id,
                "application_creator": ctx.author.id,
                "log_channel": log_channel,
                "enabled": True,
                "questions": questions,
            }
            self.client.applications.insert_one(new_application)
            embed = await embedHelper.success_embed(
                self.client, "Application form created."
            )
            embed.description = (
                "You have reached the maximum amount of questions "
                f"allowed for this application.\n{application_name} application has been created successfully."
            )
            return await ctx.channel.send(embed=embed)
        except asyncio.TimeoutError:
            embed = await embedHelper.error_embed(self.client, "No response given.")
            embed.description = (
                "```diff\n- Application canceled. You took to long to respond.```"
            )
            await ctx.channel.send(embed=embed)
            return


def setup(client):
    client.add_cog(Setup(client))

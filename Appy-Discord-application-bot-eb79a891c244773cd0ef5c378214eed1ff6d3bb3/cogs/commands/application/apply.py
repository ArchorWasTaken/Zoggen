import asyncio
import datetime
from timeit import default_timer as timer

from discord.ext import commands
from helpers import embedHelper


class Apply(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        description="Provides a list of the bots commands.",
        aliases=["applicationstart"],
    )
    async def apply(self, ctx, *args):
        self.client.live_applications.append(ctx.author.id)
        if not args:
            embed = await embedHelper.error_embed(self.client, "Unknown application.")
            embed.description = (
                "```diff\n- You must enter an application name.```\nFor a list of application names "
                f"type `{self.client.prefix}applications`"
            )
            return await ctx.channel.send(embed=embed)

        args = " ".join(args)
        find_application = await self.client.applications.find_one(
            {"guildId": ctx.guild.id, "name": args.lower()}
        )
        if not find_application:
            embed = await embedHelper.error_embed(self.client, "Unknown application.")
            embed.description = (
                f"```diff\n- No application found for the given value: {args.lower()}```\n"
                f"For a list of application names type `{self.client.prefix}applications`"
            )
            return await ctx.channel.send(embed=embed)
        elif find_application:
            embed = await embedHelper.default_embed(self.client, f"{args} application")
            embed.description = "Are you sure you want to apply?\n\n✅ = Yes\n❌ = No"
            priv_msg = await ctx.author.send(embed=embed)
            embed = await embedHelper.success_embed(self.client, "Application started!")
            embed.description = "I have sent you a direct message!"
            await ctx.channel.send(embed=embed)
            await priv_msg.add_reaction("✅")
            await priv_msg.add_reaction("❌")
            try:
                reaction, user = await self.client.wait_for(
                    "reaction_add",
                    check=lambda reaction, user: user.id == ctx.author.id
                    and str(reaction) == "✅"  # noqa W503
                    or user.id == ctx.author.id  # noqa W503
                    and str(reaction) == "❌",  # noqa W503
                    timeout=60,
                )
                if str(reaction) == "❌":
                    embed = await embedHelper.error_embed(
                        self.client, "Application canceled"
                    )
                    embed.description = "```diff\n- Application canceled.```"
                    await ctx.author.send(embed=embed)
                    return
                elif str(reaction) == "✅":
                    return await self.application_started(ctx, user, args)

            except asyncio.TimeoutError:
                embed = await embedHelper.error_embed(self.client, "Application setup")
                embed.description = (
                    "```diff\n- Application canceled. You took to long to respond.```"
                )
                await ctx.author.send(embed=embed)
                try:
                    self.client.live_applications.pop(ctx.author.id)
                except Exception:
                    pass
                return

    async def application_started(self, ctx, user, args):
        try:
            answers = {}
            embed = await embedHelper.default_embed(self.client, f"{args} Application")

            find_document = await self.client.applications.find_one(
                {"guildId": ctx.guild.id, "name": args.lower()}
            )
            if not find_document:
                embed = await embedHelper.default_embed(self.client, "Error")
                embed.description = (
                    "Error, couldn't find the application you requested."
                )
                return await ctx.author.send(embed=embed)
            length = len(find_document["questions"])
            count = 0
            start = timer()
            for question in find_document["questions"]:
                count += 1
                embed.description = f"**{count}/{length}**. {question}"
                await ctx.author.send(embed=embed)
                msg = await self.client.wait_for(
                    "message",
                    check=lambda message: message.author == ctx.author
                    and message.channel.id == user.dm_channel.id,  # noqa: W503
                    timeout=800,
                )
                if len(msg.attachments) >= 1:
                    print("heressss")
                    answers[
                        question.replace(".", "")
                    ] = f"{msg.content}{msg.attachments[0]}"
                    print(msg.attachments[0])
                    print(answers)
                else:
                    answers[question.replace(".", "")] = msg.content
        except asyncio.TimeoutError:
            embed = await embedHelper.error_embed(self.client, "Application setup")
            embed.description = (
                "```diff\n- Application canceled. You took to long to respond.```"
            )
            await ctx.author.send(embed=embed)
            try:
                self.client.live_applications.pop(ctx.author.id)
            except Exception:
                pass
            return
        elapsed_time = timer() - start
        embed_wait_confirmation = await embedHelper.default_embed(
            self.client, "Application completed."
        )
        embed_wait_confirmation.description = (
            "Attempting to submit your application now..."
        )
        embed_to_edit = await ctx.author.send(embed=embed_wait_confirmation)
        channel = self.client.get_channel(find_document["log_channel"])
        application_embed = await embedHelper.default_embed(
            self.client, f"{ctx.author}'s application for {args}"
        )
        try:
            total_char = 0
            over_max_char = False
            for answer in answers:  # answer = question
                if len(answers[answer]) > 1024:
                    over_max_char = True
                total_char += len(answers[answer])
                application_embed.add_field(
                    name=answer, value=answers[answer], inline=False
                )
            application_embed.add_field(
                name="Application duration",
                value=f"{round(elapsed_time, 2)} seconds",
                inline=False,
            )
            channel = self.client.get_channel(find_document["log_channel"])
            if total_char > 6000 or over_max_char:
                application_embed.clear_fields()
                application_embed.description = ""
                add_word_back = []
                for answer in answers:
                    print(f"0 - {len(application_embed.description)}")
                    if len(application_embed.description) >= 2000:
                        print(f"1 - {len(application_embed.description)}")
                        take_off_char_calculation = total_char - 2000
                        while application_embed.description > 2000:
                            split = application_embed.description.split()
                            add_word_back.append(split[-1])
                            split.replace(split[-1], "")
                            len(application_embed.description)
                        application_embed.description += "**...**"
                        if take_off_char_calculation == 0:
                            await ctx.channel.send(embed=application_embed)
                            continue
                        for word in add_word_back:
                            application_embed.description += word
                    application_embed.description += (
                        f"**Question:** {answer}\n**Answer:** {answers[answer]}"
                    )
                    print(f"2 - {len(application_embed.description)}")
                    await ctx.channel.send(embed=application_embed)
                    application_embed.description = ""

                print(f"3 - {len(application_embed.description)}")
                if len(embed.description) == 0:
                    return
                return await channel.send(embed=application_embed)
        except Exception as e:
            print(e)
        application_embed.add_field(
            name="Application by", value=ctx.author.mention, inline=False
        )
        application_embed.set_thumbnail(url=ctx.author.avatar_url)
        application_message = await channel.send(embed=application_embed)
        self.client.applicants.insert_one(
            {
                "name": args,
                "userId": ctx.author.id,
                "guildId": ctx.guild.id,
                "messageId": application_message.id,
                "time_created": datetime.datetime.utcnow(),
                "duration": round(elapsed_time, 2),
                "questions": answers,
            }
        )
        try:
            self.client.live_applications.pop(ctx.author.id)
        except Exception:
            pass
        try:
            await asyncio.sleep(2)
            new_embed = await embedHelper.success_embed(
                self.client, "Your application has been submitted."
            )
            new_embed.description = "Your application has been submitted successfully!"
            await embed_to_edit.edit(embed=new_embed)
        except Exception as e:
            print(e)
            embed = await embedHelper.error_embed(
                self.client, "Application failed to send."
            )
            embed.description = (
                "An error occured when trying to submit your application. "
                "Please contact <@585548631268917254> (8au#0489) for more information."
            )
            await embed_to_edit.edit(embed=embed)


def setup(client):
    client.add_cog(Apply(client))

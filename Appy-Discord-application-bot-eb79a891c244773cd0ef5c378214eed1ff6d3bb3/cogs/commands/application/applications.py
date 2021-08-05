from discord.ext import commands
from helpers import embedHelper


class Applications(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        description="Provides a list of the bots commands.",
        aliases=["listapplications", "applicationlist"],
    )
    async def applications(self, ctx):
        embed = await embedHelper.default_embed(self.client, "Your applications")
        cursor = self.client.applications
        count = 0
        found_result = False
        async for document in cursor.find({"guildId": ctx.guild.id}):
            found_result = True
            count += 1
            embed.add_field(
                name=f"Application {count}",
                value=f"`Name:` **{document['name']}**\n"
                f"`Application Creator:` <@{document['application_creator']}>\n"
                f"`Log channel:` <#{document['log_channel']}>\n"
                f"`Enabled:` **{document['enabled']}**\n",
                inline=False,
            )
        if found_result is False:
            embed = await embedHelper.error_embed(self.client, "No applications found!")
            embed.description = (
                "```diff\n- You currently do not have any applications.\n\n- "
                "To create an application type -setup```"
            )
        else:
            embed.description = (
                "```fix\nHere is a list of your current applications. "
                f"If you wish to delete an application type {self.client.prefix}delete <applicationName>```"
            )
        await ctx.channel.send(embed=embed)


def setup(client):
    client.add_cog(Applications(client))

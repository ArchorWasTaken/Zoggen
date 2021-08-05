from discord.ext import commands
from helpers import embedHelper


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(description="Provides a list of the bots commands.")
    async def help(self, ctx):
        embed = await embedHelper.default_embed(self.client, "Commands")
        for command in self.client.commands:
            if command.description == "":
                command.description = "."
            if command.usage is None:
                command.usage = ""
            embed.add_field(
                name=f"{self.client.prefix}{command.name} {command.usage}",
                value=f"```{command.description}```",
                inline=True,
            )

        await ctx.channel.send(embed=embed)


def setup(client):
    client.add_cog(Help(client))

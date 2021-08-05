import datetime

from discord.ext import commands
from helpers import embedHelper


class Stats(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(description="Shows the bots stats")
    async def stats(self, ctx):
        delta_uptime = datetime.datetime.utcnow() - self.client.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        embed = await embedHelper.default_embed(self.client, self.client.user.name)
        embed.add_field(name="Guilds", value=len(self.client.guilds), inline=True)
        embed.add_field(name="Users", value=len(self.client.users), inline=True)
        embed.add_field(
            name="Ping", value=f"{int(self.client.latency * 1000)}ms", inline=True
        )
        embed.add_field(
            name="Bot up since",
            value=f"{days}d, {hours}h, {minutes}m, {seconds}s",
            inline=True,
        )
        embed.add_field(
            name="Total commands", value=len(self.client.commands), inline=True
        )
        embed.add_field(
            name=f"{self.client.user.name} version",
            value=self.client.version,
            inline=True,
        )
        await ctx.channel.send(embed=embed)


def setup(client):
    client.add_cog(Stats(client))

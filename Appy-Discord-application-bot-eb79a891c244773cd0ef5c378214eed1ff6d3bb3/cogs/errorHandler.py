import discord
from discord.ext import commands
from helpers import embedHelper


class Errorhandling(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        error = getattr(error, "original", error)
        if isinstance(error, commands.CheckFailure):
            return
        elif isinstance(error, commands.MissingRequiredArgument):
            try:
                embed = discord.Embed(title=str(self.client.user), color=0xFF0000)
                embed.add_field(
                    name=f"Invalid parameters for {ctx.command.name} command",
                    value=f"`{error.param}` is a required argument "
                    f"which is missing.\n usage: **{ctx.command.usage}**",
                    inline=False,
                )
                await ctx.send(embed=embed)
            except discord.Forbidden:
                pass
        elif isinstance(error, commands.BadArgument):
            embed = discord.Embed(title=str(self.client.user), color=0xFF0000)
            embed.add_field(
                name=f"Unknown parameter for {ctx.command.name} command",
                value=f"{error}",
                inline=False,
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(title=str(self.client.user), color=0xFF0000)
            embed.add_field(
                name=f"Bot missing permissions for {ctx.command.name} " f"command",
                value=f"{error}",
                inline=False,
            )
            await ctx.send(embed=embed)
        elif isinstance(error, discord.Forbidden):
            try:
                embed = await embedHelper.error_embed(self.client, "Command Error")
                embed.description = (
                    f"I do not have permissions to send a "
                    f"message in {ctx.channel.mention}"
                )
                await ctx.author.send(embed=embed)
            except discord.Forbidden:
                print("Unable to send message to user.")
                await ctx.channel.send("I am unable to send you direct messages.")
        elif isinstance(error, commands.CommandNotFound):
            pass
        else:
            raise error


def setup(client):
    client.add_cog(Errorhandling(client))

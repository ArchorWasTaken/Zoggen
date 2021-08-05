from discord.ext import commands
from helpers import embedHelper


class Delete(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        description="Allows you to delete applications.",
        aliases=["deleteapplication", "del", "delapp"],
    )
    @commands.has_permissions(manage_guild=True)
    async def delete(self, ctx, *args):
        if not args:
            embed = await embedHelper.error_embed(self.client, "No arguements given")
            embed.description = (
                "```diff\n- You provided no application name to delete.```"
                "**current applications type** `-applications`"
            )
            return await ctx.channel.send(embed=embed)
        string = " ".join(args)
        find_application = await self.client.applications.find_one(
            {"name": string, "guildId": ctx.guild.id}
        )
        if not find_application:
            embed = await embedHelper.error_embed(self.client, "Delete application")
            embed.description = (
                "```diff\n- Unknown application name.\n```"
                "**current applications type** `-applications`"
            )
            return await ctx.channel.send(embed=embed)
        elif find_application:
            embed = await embedHelper.success_embed(self.client, "Delete application")
            embed.description = (
                f"```diff\n+ Successfully deleted the {string} application form!```"
            )
            await self.client.applications.delete_one({"name": string})
            if not await self.client.applications.find_one({"name": string}):
                return await ctx.channel.send(embed=embed)
            else:
                embed.description = "An unknown error occured."
                return await ctx.channel.send(embed=embed)
        else:
            print("Unknown error")


def setup(client):
    client.add_cog(Delete(client))  #

import json

import statcord
from discord.ext import commands

with open("token.json") as json_file:
    data = json.load(json_file)


class StatcordPost(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.key = data["statcord"]
        self.api = statcord.Client(self.client, self.key, custom1=self.custom1)
        self.api.start_loop()
        self.messageCount = 0

    @commands.Cog.listener()
    async def on_command(self, ctx):
        self.api.command_run(ctx)

    async def custom1(self):
        count = self.messageCount
        self.messageCount = 0
        return str(count)

    @commands.Cog.listener("on_message")
    async def on_message(self, message):
        self.messageCount += 1


def setup(client):
    client.add_cog(StatcordPost(client))

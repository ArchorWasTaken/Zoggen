import datetime
import glob
import json

import discord
import motor.motor_asyncio
from discord.ext import commands
from helpers import embedHelper

with open("token.json") as json_file:
    data = json.load(json_file)

prefixjson = data["default_prefix"]
prefix = prefixjson
intents = discord.Intents(messages=True, guilds=True, members=True, reactions=True)
client = commands.AutoShardedBot(
    command_prefix=prefixjson, intents=intents, help_command=None
)

client.prefix = prefixjson
client.version = "1.0.0"

mongo_connect = data["mongoconnect"]
client.cluster = motor.motor_asyncio.AsyncIOMotorClient(mongo_connect)
client.applications = client.cluster["Appy"]["applications"]
client.applicants = client.cluster["Appy"]["applicants"]


client.live_applications = []


@client.event
async def on_ready():
    await client.wait_until_ready()
    print("Ready")
    await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, name="Message me to invite me!"
        )
    )


async def no_guild(message):
    embed = await embedHelper.no_guild_embed(client)
    await message.channel.send(
        "Im Archor",
        embed=embed,
    )
    return


@client.listen("on_message")
async def on_message(message):
    if message.author.bot:
        return

    if message.guild is None:  # direct message - Ignore
        if message.author.id not in client.live_applications:
            return await no_guild(message)
        else:
            pass


@client.event
async def on_guild_join(guild):
    try:
        async for entry in guild.audit_logs(action=discord.AuditLogAction.bot_add):
            if entry.target == client.user:
                embed = await embedHelper.support_embed(client)
                embed.add_field(
                    name="Thank you for inviting me! 😊",
                    value="Struggling to use the bot? join our support discord here: https://discord.gg/bDmc55c6zY",
                    inline=False,
                )
                embed.add_field(
                    name="Support 🆘",
                    value="Need help? Don't hesitate to ask "
                    "us! Join [here](https://discord.gg/bDmc55c6zY)",
                    inline=False,
                )
                await entry.user.send("https://discord.gg/bDmc55c6zY", embed=embed)
                break
    except discord.Forbidden:
        pass
    channel = await client.fetch_channel(856633508105289768)
    embed = await embedHelper.guild_add_embed(client, guild)
    await channel.send(embed=embed)


@client.event
async def on_guild_remove(guild):
    channel = await client.fetch_channel(856633520223158293)
    embed = await embedHelper.guild_remove_embed(client, guild)
    await channel.send(embed=embed)


cog_list = glob.glob("cogs/**/*.*", recursive=True)

for file_path in cog_list:
    if file_path.endswith(".py"):
        file_path = file_path.replace(data["file_slash"], ".")
        file_path = file_path.replace(".py", "")
        client.load_extension(file_path)
        print(f"Loaded {file_path}")

client.launch_time = datetime.datetime.utcnow()

token = data["token"]
client.run(token)

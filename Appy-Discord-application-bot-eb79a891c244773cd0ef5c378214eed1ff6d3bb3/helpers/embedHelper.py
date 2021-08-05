import discord


async def default_embed(client, title):
    embed = discord.Embed(title=title, color=discord.colour.Color.purple())
    embed.set_author(name="Appy", icon_url=client.user.avatar_url)
    embed.set_footer(
        text="Like the bot? Consider voting for it by typing .vote (It would really help us out!)",
        icon_url=client.user.avatar_url,
    )
    return embed


async def success_embed(client, title):
    embed = discord.Embed(title=title, color=discord.colour.Color.green())
    embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/673498934798319646.gif")
    embed.set_author(name="Appy", icon_url=client.user.avatar_url)
    embed.set_footer(
        text="Like the bot? Consider voting for it by typing .vote (It would really help us out!)",
        icon_url=client.user.avatar_url,
    )
    return embed


async def error_embed(client, title):
    embed = discord.Embed(title=title, color=discord.colour.Color.red())
    embed.set_author(name="Appy", icon_url=client.user.avatar_url)
    embed.set_footer(
        text="Like the bot? Consider voting for it by typing .vote (It would really help us out!)",
        icon_url=client.user.avatar_url,
    )
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/"
        "768848054064644156/846053950036770877/3442-pepe-crydrink.gif"
    )
    return embed


async def no_guild_embed(client):
    embed = discord.Embed(title="Hello!", color=discord.colour.Color.purple())
    embed.add_field(name="Hello! 👋", value="Thanks for messaging me!", inline=False)
    embed.add_field(
        name="Inviting the bot",
        value="If you want to invite the bot, you can do so "
        "[here!](https://top.gg/bot/853327905357561948)",
        inline=False,
    )
    embed.add_field(
        name="Vote 📫",
        value="If you are feeling really kind, you can vote for "
        "our bot here in order to help support us "
        "[here](https://top.gg/bot/853327905357561948/vote)",
        inline=True,
    )
    embed.set_footer(
        text="Like the bot? Consider voting for it by typing "
        f"{client.prefix}vote (It would really help us out!)"
    )
    embed.set_thumbnail(url=client.user.avatar_url)
    return embed


async def guild_add_embed(client, guild):
    embed = discord.Embed(
        title=client.user.display_name, color=discord.colour.Color.green()
    )
    embed.set_author(name="Appy", icon_url=client.user.avatar_url)
    embed.add_field(name=f"New server - {guild.name}", value=guild.name, inline=True)
    embed.add_field(
        name="New user count",
        value=f"{len(client.users)} (+{guild.member_count})",
        inline=True,
    )
    embed.add_field(
        name="New Guild Count", value=f"{len(client.guilds)} (+1)", inline=True
    )
    embed.add_field(
        name="New Emoji Count",
        value=f"{len(client.emojis)} (+{len(guild.emojis)})",
        inline=True,
    )
    embed.set_footer(
        text="Like the bot? Consider voting for it by typing .vote (It would really help us out!)",
        icon_url=client.user.avatar_url,
    )
    return embed


async def guild_remove_embed(client, guild):
    embed = discord.Embed(
        title=client.user.display_name, color=discord.colour.Color.red()
    )
    embed.set_author(name="Appy", icon_url=client.user.avatar_url)
    embed.add_field(name=f"New server - {guild.name}", value=guild.name, inline=True)
    embed.add_field(
        name="New user count",
        value=f"{len(client.users)} (-{guild.member_count})",
        inline=True,
    )
    embed.add_field(
        name="New Guild Count", value=f"{len(client.guilds)} (-1)", inline=True
    )
    embed.add_field(
        name="New Emoji Count",
        value=f"{len(client.emojis)} (-{len(guild.emojis)})",
        inline=True,
    )
    embed.set_footer(
        text="Like the bot? Consider voting for it by typing .vote (It would really help us out!)",
        icon_url=client.user.avatar_url,
    )
    return embed


async def support_embed(client):
    embed = discord.Embed(title="Hey 👋", color=discord.colour.Color.gold())
    embed.set_author(name="Appy applications", icon_url=client.user.avatar_url)
    embed.set_footer(
        text="Created by 8au#0489",
        icon_url=client.user.avatar_url,
    )
    return embed

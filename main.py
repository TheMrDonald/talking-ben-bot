import nextcord
from nextcord import File
from nextcord.ext import tasks
from nextcord.ext import commands, application_checks
from nextcord import file, ButtonStyle, SlashOption
from nextcord.ui import Select, View, button, Button
from nextcord.interactions import Interaction
import os
import json
import urllib
import requests
import random
import asyncio
import aiosqlite
from easy_pil import *
import cooldowns

client = commands.Bot(help_command=None, intents=nextcord.Intents.all())


@client.event
async def on_ready():
    setattr(client, "db", await aiosqlite.connect("main.db"))
    async with client.db.cursor() as cs:
        await cs.execute(
            "CREATE TABLE IF NOT EXISTS levels (level INTEGER, xp INTEGER, user INTEGER, guild INTEGER)"
        )
        await cs.execute(
            "CREATE TABLE IF NOT EXISTS settings (leveling BOOL, guild INTEGER)"
        )
    await client.change_presence(activity=nextcord.Game(name="Ugh..."))
    print("Bot is ready")


#help


class Dropdown(nextcord.ui.Select):

    def __init__(self):
        selectOptions = [
            nextcord.SelectOption(
                label="Help",
                emoji="❓",
                description="View Talking Bens Help Command."),
            nextcord.SelectOption(
                label="Fun",
                emoji="🤣",
                description="View Talking Bens Fun Commands!"),
            nextcord.SelectOption(
                label="Chatbot",
                emoji="💬",
                description="View Talking Bens Chatbot Commands!"),
            nextcord.SelectOption(
                label="Audio",
                emoji="🔉",
                description="View Talking Bens Audio Commands!"),
            nextcord.SelectOption(
                label="Leveling",
                emoji="📊",
                description="View Talking Bens Leveling Commands!")
        ]
        super().__init__(placeholder="Select Menu Option",
                         min_values=1,
                         max_values=1,
                         options=selectOptions)

    async def callback(self, interaction: nextcord.Interaction):
        if self.values[0] == 'Help':
            embed = nextcord.Embed(
                title="Help Menu",
                description=
                "This is a help menu for navigating Talking Bens commands!",
                color=0xa6fc06)
            embed.add_field(
                name="/help",
                value=
                "<:ben:1022668306945151046> Recive this exact embed message.",
                inline=False)
            embed.add_field(
                name="/latency",
                value=
                "<:ben:1022668306945151046> Show talking bens latency measurements.",
                inline=False)
            embed.add_field(
                name="/support",
                value=
                "<:ben:1022668306945151046> Get an invite link to the bots support server.",
                inline=False)
            embed.add_field(
                name="/invite",
                value=
                "<:ben:1022668306945151046> Get an invite link to add the bot to your server.",
                inline=False)
            embed.set_footer(text="Page 1/5")
            await interaction.response.edit_message(embed=embed)
        if self.values[0] == 'Fun':
            embed = nextcord.Embed(
                title="Fun Menu",
                description=
                "This is a fun menu for navigating Talking Bens commands!",
                color=0xa6fc06)
            embed.add_field(
                name="/meme",
                value=
                "<:ben:1022668306945151046> Recive a meme from the reddit platform.",
                inline=False)
            embed.add_field(
                name="/ask",
                value=
                "<:ben:1022668306945151046> Ask talking ben a question about the future.",
                inline=False)
            embed.add_field(
                name="/drink",
                value=
                "<:ben:1022668306945151046> Watch talking ben drink some beer to gain extra xp.",
                inline=False)
            embed.add_field(
                name="/eat",
                value=
                "<:ben:1022668306945151046> Watch talking ben eat some beans to gain extra xp.",
                inline=False)
            embed.add_field(
                name="/slap",
                value=
                "<:ben:1022668306945151046> Slap talking ben to gain extra xp.",
                inline=False)
            embed.add_field(
                name="/echo",
                value=
                "<:ben:1022668306945151046> Bot will echo a message of yours.",
                inline=False)
            embed.set_footer(text="Page 2/5")
            await interaction.response.edit_message(embed=embed)
        if self.values[0] == 'Chatbot':
            embed = nextcord.Embed(
                title="Chatbot Menu",
                description=
                "This is a chatbot menu for navigating Talking Bens commands!",
                color=0xa6fc06)
            embed.add_field(
                name="Ben,",
                value=
                "<:ben:1022668306945151046> Ask talking ben some questions!",
                inline=False)
            embed.set_footer(text="Page 3/5")
            await interaction.response.edit_message(embed=embed)
        if self.values[0] == 'Audio':
            embed = nextcord.Embed(
                title="Audio Menu",
                description=
                "This is an audio menu for navigating Talking Bens commands!",
                color=0xa6fc06)
            embed.add_field(
                name="/no",
                value="<:ben:1022668306945151046> Hear talking ben say no.",
                inline=False)
            embed.add_field(
                name="/yes",
                value="<:ben:1022668306945151046> Hear talking ben say yes.",
                inline=False)
            embed.add_field(
                name="/ugh",
                value="<:ben:1022668306945151046> Hear talking ben say ugh.",
                inline=False)
            embed.add_field(
                name="/hoho",
                value="<:ben:1022668306945151046> Hear talking ben say hoho.",
                inline=False)
            embed.add_field(
                name="/ring",
                value=
                "<:ben:1022668306945151046> Hear talking bens phone ring.",
                inline=False)
            embed.set_footer(text="Page 4/5")
            await interaction.response.edit_message(embed=embed)
        if self.values[0] == 'Leveling':
            embed = nextcord.Embed(
                title="Leveling Menu",
                description=
                "This is an leveling menu for navigating Talking Bens commands!",
                color=0xa6fc06)
            embed.add_field(
                name="/level",
                value="<:ben:1022668306945151046> Check your server level.",
                inline=False)
            embed.add_field(
                name="/leaderboard",
                value=
                "<:ben:1022668306945151046> Check the talking ben level leaderboard.",
                inline=False)
            embed.add_field(
                name="/enable",
                value=
                "<:ben:1022668306945151046> Enable/Disable the leveling system in your server.",
                inline=False)
            embed.set_footer(text="Page 5/5")
            await interaction.response.edit_message(embed=embed)


class DropdownView(nextcord.ui.View):

    def __init__(self):
        super().__init__()
        self.add_item(Dropdown())


@client.slash_command(name="help",
                      description="Get a help menu from talking ben!")
async def help(interaction: nextcord.Interaction):
    view = DropdownView()
    embed = nextcord.Embed(
        title="Help Menu",
        description="This is a help menu for navigating Talking Bens commands!",
        color=0xa6fc06)
    embed.add_field(
        name="/help",
        value="<:ben:1022668306945151046> Recive this exact embed message.",
        inline=False)
    embed.add_field(
        name="/latency",
        value=
        "<:ben:1022668306945151046> Show talking bens latency measurements.",
        inline=False)
    embed.add_field(
        name="/support",
        value=
        "<:ben:1022668306945151046> Get an invite link to the bots support server.",
        inline=False)
    embed.add_field(
        name="/invite",
        value=
        "<:ben:1022668306945151046> Get an invite link to add the bot to your server.",
        inline=False)
    embed.set_footer(text="Page 1/5")

    await interaction.response.send_message(embed=embed, view=view)


#other


@client.slash_command(name="meme",
                      description="Upload a meme from the reddit platform!")
async def meme(interaction: Interaction):
    memeAPI = urllib.request.urlopen('https://meme-api.herokuapp.com/gimme')

    memeData = json.load(memeAPI)

    memeUrl = memeData['url']
    memeName = memeData['title']
    memeSub = memeData['subreddit']
    memeLink = memeData['postLink']

    embed = nextcord.Embed(
        title=memeName,
        description=
        f"Scraped from [r/{memeSub}](https://www.reddit.com)┃{memeLink}",
        color=0xa6fc06)
    embed.set_image(url=memeUrl)
    await interaction.response.send_message(embed=embed)


@client.slash_command(name="ask", description="Ask talking ben a question!")
async def eightball(interaction: Interaction, question):
    responses = ["Yes...", "No...", "Ugh..."]
    response = random.choice(responses)
    if response == "Yes...":
        embed = nextcord.Embed(title="Talking Ben:",
                               description=f"{response}",
                               color=0xa6fc06)
        embed.set_image(
            url="https://c.tenor.com/R_itimARcLAAAAAd/talking-ben-yes.gif")
        await interaction.response.send_message(embed=embed)
    if response == "No...":
        embed = nextcord.Embed(title="Talking Ben:",
                               description=f"{response}",
                               color=0xa6fc06)
        embed.set_image(
            url="https://c.tenor.com/3ZLujiiPc4YAAAAC/talking-ben-no.gif")
        await interaction.response.send_message(embed=embed)
    if response == "Ugh...":
        embed = nextcord.Embed(title="Talking Ben:",
                               description=f"{response}",
                               color=0xa6fc06)
        embed.set_image(
            url="https://c.tenor.com/fr6i8VzKJuEAAAAd/talking-ben-ugh.gif")
        await interaction.response.send_message(embed=embed)


@client.slash_command(name="latency",
                      description="Measure the bots ping latency.")
async def ping(i: Interaction):
    await i.response.send_message(f"Ping Rate:\n**{client.latency}**")


@client.slash_command(name="echo",
                      description="Talking ben will echo your message")
async def echo(i: Interaction, message):
    embed = nextcord.Embed(description=f"{message}", color=0xa6fc06)
    await i.response.send_message(f"{i.user.mention}", embed=embed)


@client.event
async def on_message(message):
    if client.user.mentioned_in(message):
        embed = nextcord.Embed(
            title="Ho Ho Ho Ho!",
            description=
            "It seems that I have been mentioned in a text channel!",
            color=0xa6fc06)
        await message.channel.send(embed=embed)


@client.slash_command(name="support",
                      description="Get a link to the bots support server!")
async def support(i: Interaction):
    await i.response.send_message("https://discord.gg/SsMXttzpay")


@client.slash_command(name="invite", description="Get the bots invite link!")
async def support(i: Interaction):
    embed = nextcord.Embed(
        title="Invite Me!",
        url=
        "https://discord.com/api/oauth2/authorize?client_id=1021941421302878259&permissions=8&scope=bot",
        color=0xa6fc06)
    await i.response.send_message(embed=embed)


def check(msg):
    return nextcord.Interaction.user == nextcord.Interaction.user and nextcord.Interaction.channel == nextcord.Interaction.channel


#leveling


@client.event
async def on_message(message):
    if client.user.mentioned_in(message):
        embed = nextcord.Embed(
            title="Ho Ho Ho Ho!",
            description=
            "It seems that I have been mentioned in a text channel!",
            color=0xa6fc06)
        await message.channel.send(embed=embed)
    if "Ben," in message.content:
        responses = ["ohoho", "yes...", "no...", "ugh"]
        response = random.choice(responses)
        await message.reply(f"{response}")

    if message.author.bot:
        return

    author = message.author
    guild = message.guild

    async with client.db.cursor() as cs:
        await cs.execute("SELECT leveling FROM settings WHERE guild = ?",
                         (guild.id, ))
        leveling = await cs.fetchone()
        if leveling and not leveling[0]:
            return
        await cs.execute("SELECT xp FROM levels WHERE user = ? AND guild = ?",
                         (
                             author.id,
                             guild.id,
                         ))
        xp = await cs.fetchone()
        await cs.execute(
            "SELECT level FROM levels WHERE user = ? AND guild = ?", (
                author.id,
                guild.id,
            ))
        level = await cs.fetchone()

        if not xp or not level:
            await cs.execute(
                "INSERT INTO levels (level, xp, user, guild) VALUES (?, ?, ?, ?)",
                (
                    0,
                    0,
                    author.id,
                    guild.id,
                ))

        try:
            xp = xp[0]
            level = level[0]
        except TypeError:
            xp = 0
            level = 0

        if level < 5:
            xp += random.randint(1, 4)
            await cs.execute(
                "UPDATE levels SET xp = ? WHERE user = ? AND guild = ?", (
                    xp,
                    author.id,
                    guild.id,
                ))
        else:
            rand = random.randint(1, level // 4)
            if rand == 1:
                xp += random.randint(1, 4)
                await cs.execute(
                    "UPDATE levels SET xp = ? WHERE user = ? AND guild = ?", (
                        level,
                        author.id,
                        guild.id,
                    ))
        if xp >= 100:
            level += 1
            await cs.execute(
                "UPDATE levels SET level = ? WHERE user = ? AND guild = ?", (
                    level,
                    author.id,
                    guild.id,
                ))
            await cs.execute(
                "UPDATE levels set xp = ? WHERE user = ? AND guild = ?", (
                    0,
                    author.id,
                    guild.id,
                ))
            await message.channel.send(
                f"<:images:1023065410700070932> {author.mention} has leveled up to **Level {level}!**"
            )
    await client.db.commit()

    await client.process_commands(message)


@client.slash_command(name="level",
                      description="Find out what your server level is.")
async def level(i: Interaction,
                member: nextcord.Member = SlashOption(
                    name="member",
                    description="The member to check the level of.",
                    required=False)):
    if member is None:
        member = i.user

    async with client.db.cursor() as cs:
        await cs.execute("SELECT leveling FROM settings WHERE guild = ?",
                         (i.guild.id, ))
        leveling = await cs.fetchone()
        if leveling and not leveling[0]:
            await i.response.send_message(
                "Leveling is disabled in this server!")
            return
        await cs.execute(
            "SELECT level FROM levels WHERE user = ? AND guild = ?", (
                member.id,
                i.guild.id,
            ))
        level = await cs.fetchone()
        await cs.execute("SELECT xp FROM levels WHERE user = ? AND guild = ?",
                         (
                             member.id,
                             i.guild.id,
                         ))
        xp = await cs.fetchone()
        if not level or not xp:
            await cs.execute(
                "INSERT INTO levels (level, xp, user, guild) VALUES (?, ?, ?, ?)",
                (
                    0,
                    0,
                    member.id,
                    i.guild.id,
                ))
            await client.db.commit()
        try:
            level = level[0]
            xp = xp[0]
        except TypeError:
            level = 0
            xp = 0

        data = {
            "name": f"{member.name}#{member.discriminator}'s Level",
            "xp": xp,
            "level": level,
            "next_level": 100,
            "percent": xp
        }

        bg = Editor(Canvas((900, 300), color="#31A944"))
        pfp = await load_image_async(str(member.avatar.url))
        profile = Editor(pfp).resize((150, 150)).circle_image()

        monsterrat = Font.montserrat(size=45)
        monsterrat_small = Font.montserrat(size=30)

        card_shape = [(600, 0), (750, 300), (900, 300), (900, 0)]
        bg.polygon(card_shape, color="#2F8A3D")
        bg.paste(profile, (30, 30))

        bg.rectangle((30, 220),
                     width=650,
                     height=40,
                     color="#454545",
                     radius=10)
        bg.bar((30, 220),
               max_width=650,
               height=40,
               percentage=data['percent'],
               color="#36C04B",
               radius=10)
        bg.text((200, 40), data["name"], font=monsterrat, color="#FFFFFF")
        bg.rectangle((200, 100), width=475, height=2, fill="#FFFFFF", radius=6)
        bg.text(
            (200, 130),
            f"Level - {data['level']} | XP - {data['xp']}/{data['next_level']}",
            font=monsterrat_small,
            color="#FFFFFF")

        file = nextcord.File(fp=bg.image_bytes, filename="level.png")
        await i.response.send_message(file=file)


@client.slash_command(name="enable",
                      description="Enable/Disable leveling in your server.")
@application_checks.has_permissions(manage_messages=True)
async def toggleleveling(
    i: Interaction,
    toggle: bool = SlashOption(
        name="toggle",
        description="Whether to enable or disable leveling.",
        required=True)):
    async with client.db.cursor() as cs:
        await cs.execute("SELECT leveling FROM settings WHERE guild = ?",
                         (i.guild.id, ))
        leveling = await cs.fetchone()
        if not leveling:
            await cs.execute(
                "INSERT INTO settings (leveling, guild) VALUES (?, ?)", (
                    toggle,
                    i.guild.id,
                ))
        else:
            await cs.execute(
                "UPDATE settings SET leveling = ? WHERE guild = ?", (
                    toggle,
                    i.guild.id,
                ))
        await client.db.commit()
    if toggle == True:
        await i.response.send_message("Leveling System has been enabled!")
    else:
        await i.response.send_message("Leveling System has been disabled!")


@client.slash_command(
    name="leaderboard",
    description="Find out who the top 10 users are in your server.")
async def leaderboard(i: Interaction):
    async with client.db.cursor() as cs:
        await cs.execute("SELECT leveling FROM settings WHERE guild = ?",
                         (i.guild.id, ))
        leveling = await cs.fetchone()
        if leveling and not leveling[0]:
            await i.response.send_message(
                "Leveling is disabled in this server!")
            return
        await cs.execute(
            "SELECT user, level FROM levels WHERE guild = ? ORDER BY level DESC LIMIT 10",
            (i.guild.id, ))
        leaderboard = await cs.fetchall()
        if not leaderboard:
            await i.response.send_message(
                "There are no users in the leaderboard!")
            return
        embed = nextcord.Embed(title="Leaderboard", color=0xa6fc06)
        embed.set_thumbnail(
            url=
            "https://static.wikia.nocookie.net/talkingtomthecat/images/1/16/TalkingBenTheDog.png/revision/latest?cb=20200413123418"
        )
        for user, level in leaderboard:
            user = await client.fetch_user(user)
            embed.add_field(name=f"{user.name}#{user.discriminator}",
                            value=f"Level: {level}",
                            inline=False)
        await i.response.send_message(embed=embed)


@client.slash_command(name="eat",
                      description="Watch talking ben eat for some extra xp.")
@cooldowns.cooldown(1, 21600, bucket=cooldowns.SlashBucket.author)
async def tap(i: Interaction):
    global plusxp
    plusxp = random.randint(1, 7)

    async with client.db.cursor() as cs:
        await cs.execute("SELECT leveling FROM settings WHERE guild = ?",
                         (i.guild.id, ))
        leveling = await cs.fetchone()
        if leveling and not leveling[0]:
            await i.response.send_message(
                "Leveling is disabled in this server!")
            return
        await cs.execute(
            "SELECT level FROM levels WHERE user = ? AND guild = ?", (
                i.user.id,
                i.guild.id,
            ))
        level = await cs.fetchone()
        await cs.execute("SELECT xp FROM levels WHERE user = ? AND guild = ?",
                         (
                             i.user.id,
                             i.guild.id,
                         ))
        xp = await cs.fetchone()
        if not level or not xp:
            await cs.execute(
                "INSERT INTO levels (level, xp, user, guild) VALUES (?, ?, ?, ?)",
                (
                    0,
                    0,
                    i.user.id,
                    i.guild.id,
                ))
            await client.db.commit()
        try:
            level = level[0]
            xp = xp[0]
        except TypeError:
            level = 0
            xp = 0

        if xp + plusxp >= 100:
            await cs.execute(
                "UPDATE levels SET level = ?, xp = ? WHERE user = ? AND guild = ?",
                (
                    level + 1,
                    0,
                    i.user.id,
                    i.guild.id,
                ))
            await client.db.commit()
            embed = nextcord.Embed(
                title="Yummy Beans!",
                description=
                f"You have leveled up to **Level {level + 1}**!\nYou have also received **{plusxp} XP**.",
                color=0xa6fc06)
            embed.set_image(
                url=
                "https://c.tenor.com/UZOcqAyMu4QAAAAd/talking-ben-eating.gif")
            await i.response.send_message(embed=embed)
        else:
            await cs.execute(
                "UPDATE levels SET xp = ? WHERE user = ? AND guild = ?", (
                    xp + plusxp,
                    i.user.id,
                    i.guild.id,
                ))
            await client.db.commit()
            embed = nextcord.Embed(
                title="Yummy Beans!",
                description=f"You have received **{plusxp} XP**.",
                color=0xa6fc06)
            embed.set_image(
                url=
                "https://c.tenor.com/UZOcqAyMu4QAAAAd/talking-ben-eating.gif")
            await i.response.send_message(embed=embed)


@client.slash_command(
    name="drink",
    description="Watch talking ben drink for some extra xp. (Level 3 Required)"
)
@cooldowns.cooldown(1, 21600, bucket=cooldowns.SlashBucket.author)
async def drink(i: Interaction):
    global plusxp
    plusxp = random.randint(2, 7)

    async with client.db.cursor() as cs:
        await cs.execute("SELECT leveling FROM settings WHERE guild = ?",
                         (i.guild.id, ))
        leveling = await cs.fetchone()
        if leveling and not leveling[0]:
            await i.response.send_message(
                "Leveling is disabled in this server!")
            return
        await cs.execute(
            "SELECT level FROM levels WHERE user = ? AND guild = ?", (
                i.user.id,
                i.guild.id,
            ))
        level = await cs.fetchone()
        await cs.execute("SELECT xp FROM levels WHERE user = ? AND guild = ?",
                         (
                             i.user.id,
                             i.guild.id,
                         ))
        xp = await cs.fetchone()
        if not level or not xp:
            await cs.execute(
                "INSERT INTO levels (level, xp, user, guild) VALUES (?, ?, ?, ?)",
                (
                    0,
                    0,
                    i.user.id,
                    i.guild.id,
                ))
            await client.db.commit()
        try:
            level = level[0]
            xp = xp[0]
        except TypeError:
            level = 0
            xp = 0
        if xp + plusxp >= 100:
            await cs.execute(
                "UPDATE levels SET level = ?, xp = ? WHERE user = ? AND guild = ?",
                (
                    level + 1,
                    0,
                    i.user.id,
                    i.guild.id,
                ))
            await client.db.commit()
            embed = nextcord.Embed(
                title="Tasty Beer!",
                description=
                f"You have leveled up to **Level {level + 1}**!\nYou have also received **{plusxp} XP**.",
                color=0xa6fc06)
            embed.set_image(
                url=
                "https://c.tenor.com/hdPVLfpe81cAAAAC/talking-ben-drinking.gif"
            )
            await i.response.send_message(embed=embed)
        if level < 3:
            await i.response.send_message(
                "This command requires you to be level 3 or above!")
        else:
            await cs.execute(
                "UPDATE levels SET xp = ? WHERE user = ? AND guild = ?", (
                    xp + plusxp,
                    i.user.id,
                    i.guild.id,
                ))
            await client.db.commit()
            embed = nextcord.Embed(
                title="Tasty Beer!",
                description=f"You have received **{plusxp} XP**.",
                color=0xa6fc06)
            embed.set_image(
                url=
                "https://c.tenor.com/hdPVLfpe81cAAAAC/talking-ben-drinking.gif"
            )
            await i.response.send_message(embed=embed)


@client.slash_command(
    name="slap",
    description="Slap talking ben for some extra xp. (Level 5 Required)")
@cooldowns.cooldown(1, 21600, bucket=cooldowns.SlashBucket.author)
async def drink(i: Interaction):
    global plusxp
    plusxp = random.randint(3, 9)

    async with client.db.cursor() as cs:
        await cs.execute("SELECT leveling FROM settings WHERE guild = ?",
                         (i.guild.id, ))
        leveling = await cs.fetchone()
        if leveling and not leveling[0]:
            await i.response.send_message(
                "Leveling is disabled in this server!")
            return
        await cs.execute(
            "SELECT level FROM levels WHERE user = ? AND guild = ?", (
                i.user.id,
                i.guild.id,
            ))
        level = await cs.fetchone()
        await cs.execute("SELECT xp FROM levels WHERE user = ? AND guild = ?",
                         (
                             i.user.id,
                             i.guild.id,
                         ))
        xp = await cs.fetchone()
        if not level or not xp:
            await cs.execute(
                "INSERT INTO levels (level, xp, user, guild) VALUES (?, ?, ?, ?)",
                (
                    0,
                    0,
                    i.user.id,
                    i.guild.id,
                ))
            await client.db.commit()
        try:
            level = level[0]
            xp = xp[0]
        except TypeError:
            level = 0
            xp = 0
        if xp + plusxp >= 100:
            await cs.execute(
                "UPDATE levels SET level = ?, xp = ? WHERE user = ? AND guild = ?",
                (
                    level + 1,
                    0,
                    i.user.id,
                    i.guild.id,
                ))
            await client.db.commit()
            embed = nextcord.Embed(
                title="Slapped Ben!",
                description=
                f"You have leveled up to **Level {level + 1}**!\nYou have also received **{plusxp} XP**.",
                color=0xa6fc06)
            embed.set_image(
                url=
                "https://media1.tenor.com/images/fec88461131801c3f327f1299b268215/tenor.gif?itemid=26810722"
            )
            await i.response.send_message(embed=embed)
        if level < 5:
            await i.response.send_message(
                "This command requires you to be level 5 or above!")
        else:
            await cs.execute(
                "UPDATE levels SET xp = ? WHERE user = ? AND guild = ?", (
                    xp + plusxp,
                    i.user.id,
                    i.guild.id,
                ))
            await client.db.commit()
            embed = nextcord.Embed(
                title="Slapped Ben!",
                description=f"You have received **{plusxp} XP**.",
                color=0xa6fc06)
            embed.set_image(
                url=
                "https://media1.tenor.com/images/fec88461131801c3f327f1299b268215/tenor.gif?itemid=26810722"
            )
            await i.response.send_message(embed=embed)


#welcome

@client.event
async def on_member_join(member):
  channel = member.guild.system_channel

  await channel.send(f"Welcome {member.mention}, Our staff team hopes that you have an amazing time here at this server!")
  

  
#audio

client.run(os.environ["token"])

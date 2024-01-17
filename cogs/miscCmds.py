import discord
from discord import app_commands
from discord.ext import commands
import requests
import random
import time
from bs4 import BeautifulSoup
import wikipediaapi
from gtts import gTTS
from FFmpegPCMAudioGTTS import FFmpegPCMAudioGTTS
from io import BytesIO
import asyncio

last_message_deleted = ["Nobody deleted anything bro."]


class miscCmds(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.responses = [
            "wow that was stupid!",
            "thanks, you too!",
            "that's wonderful!",
            "not much, hbu?",
            "...",
            ":)",
            "woo!",
            "bruh",
            "who cares...",
            "lmao",
            "yes!",
            "no.",
            "maybe?",
            "idk",
            "great!",
            "i hope you have a great day!",
            "wake up",
            ":wave:",
            "how insightful!",
            "somebody once told you that the world was gonna roll you, and that was me :)"
        ]

    @app_commands.command(name="ping", description="This is a test command bozo.")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Pong! :ping_pong: {round(self.bot.latency*1000,2)}ms")

    @app_commands.command(name="snipe", description="See the last message someone deleted! YOUR SECRETS ARE MINE MUHAHAHAHAHA")
    async def snipe(self, interaction: discord.Interaction):
        global last_message_deleted
        if random.randint(1, 10) == 10:
            await interaction.response.send_message("Oopsie I forgot, better luck next time!")
        else:
            await interaction.response.send_message(last_message_deleted[0])
        if len(last_message_deleted) != 1:
            last_message_deleted.pop(0)

    @app_commands.command(name="wiki", description="Generate a random wikipedia page!")
    async def wiki(self, interaction: discord.Interaction):
        url = requests.get("https://en.wikipedia.org/wiki/Special:Random")
        soup = BeautifulSoup(url.content, "html.parser")
        title = soup.find(class_="firstHeading").text
        wiki_wiki = wikipediaapi.Wikipedia(
            'Time_God (jadenjsuh@gmail.com)', 'en')
        page = wiki_wiki.page(title)
        await interaction.response.send_message(page.fullurl)

    @app_commands.command(name="coinflip", description="Flips a coin... duh")
    async def coinflip(self, interaction: discord.Interaction):
        await interaction.response.send_message("Flipping a coin in 5 seconds... :coin:")
        for i in reversed(range(1, 5)):
            await interaction.channel.send(i)
            time.sleep(1)
        if random.randint(1, 2) == 1:
            await interaction.channel.send(file=discord.File('heads.png'))
        else:
            await interaction.channel.send(file=discord.File('tails.png'))

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        global last_message_deleted
        last_message_deleted.insert(
            0, f"<@{message.author.id}> typed: {message.content}")

    @commands.Cog.listener()
    async def on_message(self, message):
        # This is so Time God can react to Sisyphus when pinged.
        if message.author.bot:
            return

        if self.bot.user.mentioned_in(message):
            await message.reply(
                self.responses[random.randint(0, (len(self.responses)-1))]
            )

    @app_commands.command(name="timetts", description="Time God's version of TTS")
    async def timetts(self, interaction: discord.Interaction, message: str):
        tts = gTTS(text=message, lang="en")
        tts_fp = BytesIO()
        tts.write_to_fp(tts_fp)
        tts_fp.seek(0)
        await interaction.response.send_message("Playing tts message!", ephemeral=True)
        voice_channel = await interaction.user.voice.channel.connect()
        time.sleep(1)
        voice_channel.play(FFmpegPCMAudioGTTS(
            tts_fp.read(), pipe=True), after=print("Done"))
        while voice_channel.is_playing():
            await asyncio.sleep(1)
        await voice_channel.disconnect()

    @app_commands.command(name="advice", description="Don't know what to do? Ask Time God, maybe he'll know?")
    async def advice(self, interaction: discord.Interaction):
        r = requests.get(url="https://api.adviceslip.com/advice")
        data = r.json()
        advice = data["slip"]["advice"]
        await interaction.response.send_message(advice)


async def setup(bot: commands.Bot):
    await bot.add_cog(miscCmds(bot))

# Testing discord.py
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks
load_dotenv()
TOKEN = os.getenv("discord_token")
GUILD = discord.Object(id=910765409639211029)


class MyBot(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix="$",
            intents=discord.Intents.all(),
            application_id=768720737405501440)

    async def setup_hook(self):
        await self.load_extension(f"cogs.miscCmds")
        await self.load_extension(f"cogs.miscTasks")
        await self.load_extension(f"cogs.openAI")
        # await self.load_extension(f"cogs.bandCog")
        await self.load_extension(f"cogs.reminderCog")
       # await self.load_extension(f"cogs.gdCog")
        await bot.tree.sync()

    async def on_ready(self):
        print(f'{self.user} is connected!')


bot = MyBot()
bot.run(TOKEN)

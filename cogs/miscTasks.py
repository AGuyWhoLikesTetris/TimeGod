import discord
from discord.ext import tasks, commands
import time
import random
import randfacts
from datetime import datetime
import json


class miscTasks(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.messages = [
            "Hello <@1195217480587681854>!",
            "<@1195217480587681854>, more like Sisy**sus**",
            "<@1195217480587681854>, how is that boulder treating you?",
            "What are you doing right now <@1195217480587681854>?"
        ]

    @commands.Cog.listener()
    async def on_ready(self):
        self.change_time_presence.start()
        self.balls.start()
        self.sendFunFact.start()
        self.sisyphusMessage.start()

    @tasks.loop(seconds=5.0)
    async def change_time_presence(self):
        time_string = time.strftime("%I:%M:%S%p")
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="the time, it's %s PT" % (time_string)))

    @tasks.loop(seconds=60.0)
    async def balls(self):
        if random.randint(0, 10000) == 10000:
            await self.bot.get_channel(910765409639211032).send('balls')
        elif random.randint(0, 10000) == 10000:
            await self.bot.get_channel(910765409639211032).send('boobs')
        elif random.randint(0, 10000) == 10000:
            await self.bot.get_channel(910765409639211032).send('personality ;)')

    @tasks.loop(seconds=60.0)
    async def sendFunFact(self):
        current_time = datetime.now()
        if current_time.hour == 7 and current_time.minute == 0:
            message = randfacts.get_fact()
            await self.bot.get_channel(1131740192890441738).send(
                f"Yo guys, did you know that, {message}")

    @tasks.loop(seconds=60.0)
    async def sisyphusMessage(self):
        if random.randint(0, 5000) == 5000:
            await self.bot.get_channel(910765409639211032).send(
                self.messages[random.randint(0, (len(self.messages)-1))]
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(miscTasks(bot))

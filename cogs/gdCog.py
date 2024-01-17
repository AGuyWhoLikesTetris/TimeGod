import discord
from discord import app_commands
from discord.ext import tasks, commands
import requests
import time
from steam.client import SteamClient


class gdCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.last_upd_pub = 1511222225
        self.last_upd_beta = 1702269429

    @commands.Cog.listener()
    async def on_ready(self):
        self.check_steam.start()

    @tasks.loop(seconds=15.0)
    async def check_steam(self):
        # r = requests.get(url="https://api.steamcmd.net/v1/info/322170")
        client = SteamClient()
        client.anonymous_login()
        client.verbose_debug = False
        data = client.get_product_info(apps=[322170], timeout=1)
        last_upd_pub = int(data["apps"][322170]["depots"]
                           ["branches"]["public"]["timeupdated"])
        last_upd_beta = int(data["apps"][322170]["depots"]
                            ["branches"]["beta"]["timeupdated"])
        print(data)
        if last_upd_pub != self.last_upd_pub:
            for i in range(5):
                await self.bot.get_channel(732842504248098878).send("@everyone check steam :)")
                time.sleep(5)
            self.last_upd_pub = last_upd_pub
        if last_upd_beta != self.last_upd_beta:
            await self.bot.get_channel(732842504248098878).send("@everyone GD BETA BRANCH UPDATED")
            self.last_upd_beta = last_upd_beta


async def setup(bot: commands.Bot):
    await bot.add_cog(gdCog(bot))

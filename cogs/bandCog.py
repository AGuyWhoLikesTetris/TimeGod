import discord
from discord import app_commands
from discord.ext import tasks, commands
import requests
from datetime import datetime


class bandCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.access_token = "ZQAAAdI6grbq6OVQvbCHkxNMP2ZgLLVRNCTZ7YXUjEJaUq5ca3Bs2LpA9wNt2KrUsuecV7yhgyfGgn-AzsERFjcWlEtP_Kc4_fDiwZNP25QmmxiC"
        self.band_id = "AADvj-9U5qYVG_7MYv6jZHna"
        self.message_time = 0

    @app_commands.command(name="band", description="Look at most recent message from Band app")
    async def band(self, interaction: discord.Interaction, message_index: int = 0):
        if interaction.guild_id == 910765409639211029:
            URL = "https://openapi.band.us/v2/band/posts"
            PARAMS = {'access_token': self.access_token,
                      'band_key': self.band_id, 'locale': "en_US"}
            r = requests.get(url=URL, params=PARAMS)
            data = r.json()
            message = data['result_data']['items'][message_index]
            author = message['author']['name']
            photos = message['photos']
            date = datetime.fromtimestamp(
                message['created_at']/1000).strftime("%m-%d-%Y %I:%M:%S%p")
            message_content = message['content']
            discord_text = f"On {date}, {author} said,\n{message_content}"
            for photo in photos:
                discord_text += f" {photo['url']}"
            await interaction.response.send_message(discord_text)
        else:
            await interaction.response.send_message("You must be in the band server for this command to work.", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(bandCog(bot))

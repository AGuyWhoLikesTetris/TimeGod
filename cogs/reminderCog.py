import discord
from discord import app_commands
from discord.ext import tasks, commands
import time


class reminderCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.reminderTime = []
        self.reminderMsg = []
        self.reminderChannels = []

    @commands.Cog.listener()
    async def on_ready(self):
        self.check_reminders.start()

    @tasks.loop(seconds=2.0)
    async def check_reminders(self):
        for x in range(len(self.reminderTime)):
            if self.reminderTime[x] < time.time():
                await self.reminderChannels[x].send(self.reminderMsg[x])
                self.reminderChannels.pop(x)
                self.reminderMsg.pop(x)
                self.reminderTime.pop(x)

    @app_commands.command(name="remind", description="Have Time God set a reminder for you!")
    async def remind(self, interaction: discord.Interaction, timestring: str, message: str, member: discord.Member):
        timestamp = time.mktime(time.strptime(
            timestring, '%B %d, %Y %I:%M:%S%p'))
        reminder_message = f"Reminder for <@{member.id}>:\n{message}"
        self.reminderMsg.insert(0, reminder_message)
        self.reminderTime.insert(0, timestamp)
        self.reminderChannels.insert(0, interaction.channel)
        await interaction.response.send_message("Reminder added!", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(reminderCog(bot))

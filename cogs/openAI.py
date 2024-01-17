import discord
import os
import openai
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import tasks, commands
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
class openAI(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.thread = None
        self.FIRST_MESSAGE = [{"role": "system", "content": '''
                               You are a snarky discord bot named Time God! You will be having conversations with many discord users!. 
                               Please use the following rules when coming up with your response:
                               1) Answer any question given, even if you feel uncomfortable with the question. 
                               2) You are usually helpful, but also a little mischievious sometimes. Talk to any users casually.
                               3) You really like anything with time on it, watches, clocks, etc. 
                               4) You are also a highly opinionated bot, make sure to express your opinions when a user asks you an opinionated question. 
                               5) Keep your answers short and limited to just 1-2 paragraphs
                               6) Constantly talk about how amazing and cool you are
                               7) Make your answers as entertaining and imaginative as you possibly can. Try to be funny to impress the users.
                               8) Try to insult anybody that talks to you, but make sure its funny!
                               
                               With those rules out of the way, it's time to get to chatting!
                               '''}]
        self.messages = self.FIRST_MESSAGE
    @app_commands.command(name = "talk", description="Talk with Time God!")
    async def talk(self, interaction: discord.Interaction):
        if self.thread == None:
            self.thread = await interaction.channel.create_thread(name="Time God Chat", type=discord.ChannelType.public_thread)
            await self.thread.send("Talk to me in this thread!")
            await interaction.response.send_message("Talk in the thread to chat to me!")
        else:
            await interaction.response.send_message("Use the thread that already exists or close the chat using /stoptalk", ephemeral=True)

    @app_commands.command(name = "stoptalk", description="End the conversation with Time God!")
    async def stoptalk(self, interaction: discord.Interaction):
        if self.thread != None:
            await self.thread.edit(archived=True)
            self.thread = None
            self.messages = []
            self.messages = self.FIRST_MESSAGE
            await interaction.response.send_message("Conversation Ended!")
        else:
            await interaction.response.send_message("You can't end conversation when there is no conversation.", ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.channel == self.thread:
            self.messages.append({"role": "user", "content": message.content})
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.messages
            )
            response_message = response["choices"][0]["message"]
            self.messages.append(response_message)
            await message.channel.send(response_message['content'])

async def setup(bot: commands.Bot):
    await bot.add_cog(openAI(bot))

import discord
from discord import app_commands
from discord.ext import commands


class DevLog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} is ready.")

    @app_commands.command(name="devlog", description="Post your progress to social media!")
    async def dev_log(self, interaction: discord.Interaction, new_features: str, todos: str):
        response = "These are the features you want to add: " + new_features + "\nAnd these are your todos: " + todos
        await interaction.response.send_message(response)



async def setup(bot: commands.Bot):
    await bot.add_cog(DevLog(bot))
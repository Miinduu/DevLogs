import logging
import aiofiles

import discord
from discord import app_commands
from discord.ext import commands

logger = logging.getLogger("Discord")


class DevLog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} is ready.")
        logger.error("NOOOOO")

    @app_commands.command(
        name="devlog", description="Post your progress to social media!"
    )
    async def dev_log(
        self,
        interaction: discord.Interaction,
        new_features: str,
        todos: str,
        attachment: discord.Attachment,
    ):
        response = (
            "These are the features you want to add: "
            + new_features
            + "\nAnd these are your todos: "
            + todos
        )

        if attachment:
            await save_file(attachment=attachment)

        await interaction.response.send_message(response)


async def save_file(attachment: discord.Attachment):
    if not attachment:
        logger.error("No attachment provided")

    async with aiofiles.open("/home/mind/learning/devLogs/tmp/myVideo.mp4", "wb") as fp:
        try:
            await attachment.save(fp)
        except (discord.HTTPException, discord.NotFound) as e:
            logger.error(f"Could not save file: {e}")



async def setup(bot: commands.Bot):
    await bot.add_cog(DevLog(bot))

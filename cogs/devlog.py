import logging
from pathlib import Path

import discord
from discord import app_commands
from discord.ext import commands

from platforms.twitter_post import Twitter

logger = logging.getLogger("Discord")
file_path = Path("/home/mind/learning/devLogs/tmp/myVideo.mp4")


class DevLog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.twitter = Twitter(name="TwitterName", videoPath=file_path)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} is ready.")

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

        result = self.twitter.post(new_features, bool(attachment))

        logger.error(f"Posted result: {result}")

        await interaction.response.send_message(response)


async def save_file(attachment: discord.Attachment):
    if not attachment:
        logger.error("No attachment provided")

    try:
        await attachment.save(file_path)
    except (discord.HTTPException, discord.NotFound) as e:
        logger.error(f"Could not save file: {e}")


async def setup(bot: commands.Bot):
    await bot.add_cog(DevLog(bot))

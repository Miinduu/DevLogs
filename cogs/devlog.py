import datetime
import logging
import os
from pathlib import Path

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

from platforms.twitter_post import Twitter

load_dotenv()
my_user_id = os.getenv("my_user_id")

logger = logging.getLogger("Discord")
file_path = Path("/home/mind/learning/devLogs/tmp/myVideo.mp4")


class DevLog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.twitter = Twitter(name="TwitterName", videoPath=file_path)

    async def check_if_it_is_me(interaction: discord.Interaction) -> bool:
        user_id = str(interaction.user.id)
        isMe = user_id == my_user_id
        return isMe

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} is ready.")

    @app_commands.command(
        name="devlog", description="Post your progress to social media!"
    )
    @app_commands.check(check_if_it_is_me)
    async def dev_log(
        self,
        interaction: discord.Interaction,
        new_features: str,
        todos: str,
        attachment: discord.Attachment,
    ):

        if attachment:
            await save_file(attachment=attachment)

        uploadAttachment = bool(attachment)
        result = self.twitter.post(new_features, uploadAttachment)
        logger.error(f"Posted result: {result}")

        file = await attachment.to_file()
        response = f"""
            Date: {getReadableDate()}
            \nPlanned features: {new_features}
            \nTODOS: {todos}
            """
        await interaction.response.send_message(response, file=file)


async def save_file(attachment: discord.Attachment):
    if not attachment:
        logger.error("No attachment provided")

    try:
        await attachment.save(file_path)
    except (discord.HTTPException, discord.NotFound) as e:
        logger.error(f"Could not save file: {e}")


async def setup(bot: commands.Bot):
    await bot.add_cog(DevLog(bot))


def getReadableDate():
    return datetime.now().strftime("%Y-%m-%d")

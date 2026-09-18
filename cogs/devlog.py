import logging
import os
from datetime import datetime, timezone
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
        new_features: str | None = None,
        todos: str | None = None,
        attachment: discord.Attachment | None = None,
    ):
        await interaction.response.defer()
        if not new_features and not todos and not attachment:
            await interaction.response.send_message("No inputs were provided")
            return

        if attachment:
            await save_file(attachment=attachment)
        uploadAttachment = bool(attachment)

        file = await attachment.to_file()
        response = [f"Date: {getReadableDate()}"]
        if new_features:
            response.append(f"Features: {new_features}")
        if todos:
            response.append(f"TODOs: {todos}")

        isTweeted = self.twitter.post(response, uploadAttachment)
        response.append(f"-# Tweet: {'success' if isTweeted else 'failed'}")

        fileSize = os.path.getsize(file_path)
        if fileSize <= interaction.filesize_limit:
            response = "\n".join(response)
            await interaction.followup.send(response, file=file)
        else:
            response.append(
                f"-# Filesize too big to upload to discord: {human_readable_size(fileSize)}"
            )
            response = "\n".join(response)
            await interaction.followup.send(response)


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
    return datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")


def human_readable_size(size):
    if size < 1000:
        return f"{size} B"
    elif size < 1000**2:
        return f"{size / 1000:.1f} KB"
    elif size < 1000**3:
        return f"{size / 1000**2:.1f} MB"
    else:
        return f"{size / 1000**3:.1f} GB"

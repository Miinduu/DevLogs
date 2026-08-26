import asyncio
import logging
import os
from typing import cast

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = str(os.getenv("discord_token"))
CHANNEL_ID = cast(int, os.getenv("channel_id"))

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
discord.utils.setup_logging(level=logging.INFO, root=False)


@bot.event
async def on_ready():
    # await syncBot()
    print("Bot is ready")
    print("------")


async def syncBot():
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} commands")
    if not synced:
        print("No commands were synced.")


async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main():
    await load_extensions()
    await bot.start(DISCORD_TOKEN)


asyncio.run(main())

import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from utils.log import setup_logger
import logging
import pathlib
import asyncio

load_dotenv()
setup_logger()

botToken = os.getenv("DISCORDTOKEN")

logger = logging.getLogger(__name__)
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="%", help_command=None, case_insensitive=True, intents=intents)

@bot.event
async def on_ready():
    logger.info(f"Bot logged as {bot.user}")
    await bot.tree.sync()

async def main():
    extensionPaths = pathlib.Path("src/extensions")
    for file in extensionPaths.glob("*.py"):
        if file.name.startswith("__"):
            continue
        module = f"extensions.{file.stem}"
        try: 
            await bot.load_extension(module)
            logger.info(f"Extension loaded: {module}")
        except Exception as error:
            logger.info(f"Erro {module}: {error}")
    await bot.start(botToken)
    
if __name__ == "__main__":
    asyncio.run(main())
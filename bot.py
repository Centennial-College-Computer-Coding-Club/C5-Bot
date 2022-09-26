"""Discord bot for the Software Engineering Tech (SET) server 'The Codehort'."""

import os
import random
import platform
import asyncio
import disnake
from disnake.ext import commands, tasks
from dotenv import load_dotenv


if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


guild_ids = [1016871747200495646]
intents = disnake.Intents.default()
intents.members = True
intents.message_content = True
intents.guilds = True
bot = commands.Bot(command_prefix="/", intents=intents)


@tasks.loop(seconds=1800)
async def change_presence():
    presence_messages = [
        "with integral server structures",
        "annoying sounds - beep beep boop",
        "techno beats",
        "the theremin",
        "with new commands in the codehort",
    ]
    await bot.wait_until_ready()
    await bot.change_presence(activity=disnake.Activity(name=random.choice(presence_messages),
                                                        type=disnake.ActivityType.playing))


if __name__ == '__main__':
    load_dotenv()
    TOKEN = os.environ.get('DISCORD_TOKEN')
    bot.load_extensions('cogs')
    change_presence.start()
    bot.run(TOKEN)

import discord
from discord.ext import commands
import os
import asyncio
from keep_alive import keep_alive
import dotenv

dotenv.load_dotenv()

bot_token = os.getenv('TOKEN')
client = commands.Bot(command_prefix='*', help_command=None, intents=discord.Intents.all())

@client.event
async def on_ready():
    for guild in client.guilds:
        print(f'{guild.name}: {guild.id}')

    with open('image.webp', 'rb') as image:
        await client.user.edit(avatar=image.read())

async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")

keep_alive()

async def main():
    async with client:
        await load_extensions()
        await client.start(bot_token)

asyncio.run(main())

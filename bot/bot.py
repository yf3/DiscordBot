import asyncio
from pathlib import Path
import discord
from discord.ext import commands
from decouple import config

class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    async def on_command_error(self, ctx, error, /) -> None:
        await ctx.send(error)

async def add_cogs():
    for cog in [p.stem for p in Path('.').glob('*/Cogs/*.py')]:
        try:
            await bot.load_extension(f'Cogs.{cog}')
        except commands.NoEntryPointError:
            continue

async def main():
    await add_cogs()
    await bot.start(config('DISCORD_BOT_TOKEN'))

if __name__== '__main__':
    intents = discord.Intents.all()
    bot = MyBot(command_prefix='!', intents=intents)
    asyncio.run(main())

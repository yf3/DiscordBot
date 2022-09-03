import asyncio
from pathlib import Path
import discord
from discord.ext import commands
from decouple import config

class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print('Bot ready.')

    async def on_command_error(self, ctx, error: Exception, /) -> None:
        await ctx.reply(error)
        print(error.__class__)
        if isinstance(error, commands.MissingRequiredArgument):
            correct_usage = f'{self.command_prefix}{ctx.command.name} {ctx.command.signature}'
            await ctx.reply(f'correct usage: {correct_usage}')

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
    intents.presences = False
    intents.typing = False
    bot = MyBot(command_prefix='!', intents=intents)
    asyncio.run(main())

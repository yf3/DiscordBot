import asyncio
from pathlib import Path
import logging
import discord
from discord.ext import commands
from decouple import config

class MyBot(commands.Bot):
    def __init__(self, command_prefix: str, *, intents: discord.Intents) -> None:
        super().__init__(command_prefix, intents=intents)

    def _log_error(self, error: Exception):
        logging.log(logging.ERROR, error)
        logging.log(logging.ERROR, error.__class__)

    async def on_ready(self):
        logging.log(logging.INFO, 'Bot ready.')

    async def on_command_error(self, ctx, error: Exception, /) -> None:
        await ctx.reply(error)
        self._log_error(error)
        if isinstance(error, commands.MissingRequiredArgument):
            correct_usage = f'{self.command_prefix}{ctx.command.name} {ctx.command.signature}'
            await ctx.reply(f'correct usage: {correct_usage}')

async def add_cogs(bot):
    for cog in [p.stem for p in Path('.').glob('*/Cogs/*.py')]:
        try:
            await bot.load_extension(f'Cogs.{cog}')
        except commands.NoEntryPointError:
            continue

def get_intents():
    intents = discord.Intents.all()
    intents.presences = False
    intents.typing = False
    return intents

async def main():
    discord.utils.setup_logging(level=logging.INFO)
    bot = MyBot(command_prefix='!', intents=get_intents())
    await add_cogs(bot)
    await bot.start(config('DISCORD_BOT_TOKEN'))

if __name__== '__main__':
    asyncio.run(main())

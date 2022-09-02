import asyncio
from pathlib import Path
import discord
from discord.ext import commands, tasks
from decouple import config

class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
    
    async def setup_hook(self) -> None:
        self.broadcasting_task.start()
        # self.loop.create_task(self.predefined_task()) # unable to find broadcast channel

    @tasks.loop(seconds=1.0, count=2)
    async def broadcasting_task(self):
        target_channel = discord.utils.get(self.get_all_channels(), guild__name='forTestingOnly', name='forbroadcast')
        if target_channel is None:
            print('Not found')
        else:
            await target_channel.send('broadcasting')

    @broadcasting_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()

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

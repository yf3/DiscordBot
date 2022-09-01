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
            print('Not found\n')
        else:
            await target_channel.send('broadcasting')

    @broadcasting_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()

intents = discord.Intents.all()
bot = MyBot(command_prefix='!', intents=intents)

@bot.command()
async def newchannel(ctx, channel_name=None):
    current_guild = ctx.guild
    if channel_name is None:
        channel_name = "new-channel"
    await ctx.send(f'{channel_name} successfully created!')
    await current_guild.create_text_channel(channel_name)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(error)

async def add_cogs():
    # await bot.add_cog(Interactions(bot))
    # await bot.add_cog(MemberManagement(bot))
    for cog in [p.stem for p in Path('.').glob('*/Cogs/*.py')]:
        await bot.load_extension(f'Cogs.{cog}')

async def main():
    await add_cogs()
    await bot.start(config('DISCORD_BOT_TOKEN'))

if __name__== '__main__':
    asyncio.run(main())

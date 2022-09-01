import asyncio
import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions
from decouple import config

intents = discord.Intents.all()

class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
    
    async def setup_hook(self) -> None:
        self.predefined_task.start()
        # self.loop.create_task(self.predefined_task()) # unable to find broadcast channel

    @tasks.loop(seconds=1.0, count=2)
    async def predefined_task(self):
        target_channel = discord.utils.get(self.get_all_channels(), guild__name='forTestingOnly', name='forbroadcast')
        if target_channel is None:
            print('Not found\n')
        else:
            await target_channel.send('broadcasting')

    @predefined_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()

bot = MyBot(command_prefix='!', intents=intents)

class Interactions(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @commands.command()
    async def echo(self, ctx, message_content):
        await ctx.send(f'{ctx.author}:{message_content}')

@bot.command()
@has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'Bye {member} lol')

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author} has no permission to kick member!')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Kick who?')

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
    await ctx.send(f'{error} \ncorrect usage: {bot.command_prefix}{ctx.command.name} {ctx.command.signature}')

async def add_cogs():
    await bot.add_cog(Interactions(bot))

async def main():
    await add_cogs()
    await bot.start(config('DISCORD_BOT_TOKEN'))

if __name__== '__main__':
    asyncio.run(main())

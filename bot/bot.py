import asyncio
import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions
from decouple import config

intents = discord.Intents.all()

class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    async def setup_hook(self) -> None:
        self.predefined_task.start()

    @tasks.loop(seconds=3.0, count=5)
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

@bot.command()
async def echo(ctx, message_content): # ctx:commands.context
    await ctx.send(f'{ctx.author}:{message_content}')

@echo.error
async def echo_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'No message to echo!')

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
        await ctx.send(f'No such command: {ctx.message.content}')
    await ctx.send(f'correct usage: {ctx.command.signature}')


bot.run(config('DISCORD_BOT_TOKEN'))

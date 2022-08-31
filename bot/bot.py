import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions
from decouple import config

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def echo(ctx, message):
    await ctx.send(f'{ctx.author}:{message}')

@echo.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('No message to echo!')

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
        await ctx.send('kick who?')

@bot.command()
async def newchannel(ctx, channel_name=None):
    current_guild = ctx.message.guild
    if channel_name is None:
        channel_name = "new-channel"
    await ctx.send(f'{channel_name} successfully created!')
    await current_guild.create_text_channel(channel_name)

@tasks.loop(minutes=1)
async def predefined_task():
    pass

bot.run(config('DISCORD_BOT_TOKEN'))

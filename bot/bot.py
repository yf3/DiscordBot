import discord
from discord.ext import commands
from decouple import config

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def echo(ctx, message):
    await ctx.send(f'{ctx.author}:{message}')

@echo.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send('No message to echo!')
    
@bot.command()
async def kick(ctx):
    await ctx.send(content='kick?!')

bot.run(config('DISCORD_BOT_TOKEN'))

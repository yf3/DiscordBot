import discord
from discord.ext import commands
from discord import guild
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

@bot.command()
async def newChannel(ctx, channel_name):
    current_guild = ctx.message.guild
    await ctx.send(f'{channel_name} successfully created!')
    await current_guild.create_text_channel(channel_name)

bot.run(config('DISCORD_BOT_TOKEN'))

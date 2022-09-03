from discord.ext import commands

class Interactions(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(brief='Arg:message')
    async def echo(self, ctx, message_content: str = commands.parameter(description=' - Any text')):
        await ctx.send(f'{ctx.author}:{message_content}')

    @commands.command()
    async def newchannel(self, ctx, channel_name: str = commands.parameter(default=None,
                        description=' - Name of new channel, will be new-channel if not given')):
        current_guild = ctx.guild
        if channel_name is None:
            channel_name = "new-channel"
        await ctx.reply(f'Textchannel {channel_name} successfully created!')
        await current_guild.create_text_channel(channel_name)

async def setup(bot):
    await bot.add_cog(Interactions(bot))

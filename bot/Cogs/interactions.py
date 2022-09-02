from discord.ext import commands

class Interactions(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @commands.command()
    async def echo(self, ctx, message_content):
        await ctx.send(f'{ctx.author}:{message_content}')

    @commands.command()
    async def newchannel(self, ctx, channel_name=None):
        current_guild = ctx.guild
        if channel_name is None:
            channel_name = "new-channel"
        await ctx.send(f'{channel_name} successfully created!')
        await current_guild.create_text_channel(channel_name)

    async def cog_command_error(self, ctx, error: Exception) -> None:
        if isinstance(error, commands.MissingRequiredArgument):
            correct_usage = f'{self.bot.command_prefix}{ctx.command.name} {ctx.command.signature}'
            await ctx.send(f'{error} \ncorrect usage: {correct_usage}')

async def setup(bot):
    await bot.add_cog(Interactions(bot))

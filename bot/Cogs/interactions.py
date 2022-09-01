from discord.ext import commands

class Interactions(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @commands.command()
    async def echo(self, ctx, message_content):
        await ctx.send(f'{ctx.author}:{message_content}')

    async def cog_command_error(self, ctx, error: Exception) -> None:
        if isinstance(error, commands.MissingRequiredArgument):
            correct_usage = f'{self.bot.command_prefix}{ctx.command.name} {ctx.command.signature}'
            await ctx.send(f'{error} \ncorrect usage: {correct_usage}')

async def setup(bot):
    await bot.add_cog(Interactions(bot))

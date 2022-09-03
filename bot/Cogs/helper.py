from discord.ext import commands

class Helper(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

async def setup(bot):
    await bot.add_cog(Helper(bot))

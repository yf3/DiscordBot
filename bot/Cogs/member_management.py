from discord.ext import commands
from discord.ext.commands import has_permissions
from discord import Member

class MemberManagement(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @commands.command()
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member: Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'{member} is out!')

    async def cog_command_error(self, ctx, error: Exception) -> None:
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{ctx.author} has no permission to {ctx.command.name} member!')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.command.name} who?')

async def setup(bot):
    await bot.add_cog(MemberManagement(bot))
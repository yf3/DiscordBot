from discord.ext import commands
from discord.ext.commands import has_permissions
from discord import Member

class MemberManagement(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member: Member = commands.parameter(description=' - Tag a member'),
                     *, reason: str=  commands.parameter(default=None, description='(Optional)')):
        await member.kick(reason=reason)
        await ctx.send(f'{member} is out!')

    @commands.command()
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member: Member = commands.parameter(description=' - Tag a member'),
                     *, reason: str=  commands.parameter(default=None, description='(Optional)')):
        await member.ban(reason=reason)
        await ctx.send(f'{member} is banned!')

    # async def cog_command_error(self, ctx, error: Exception) -> None:
    #     if isinstance(error, commands.MissingPermissions):
    #         await ctx.reply(f'{ctx.author} has no permission to {ctx.command.name} member!')

async def setup(bot):
    await bot.add_cog(MemberManagement(bot))

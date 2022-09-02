from discord import utils
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions

class Broadcaster(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.target_channel = None

    def bdsetup(self, target_guild_name, target_channel_name):
        target_channel = utils.get(self.bot.get_all_channels(), guild__name=target_guild_name, name=target_channel_name)
        if target_channel is not None:
            self.target_channel = target_channel

    @tasks.loop(seconds=1.0, count=2)
    async def broadcast_by_name(self):
        await self.target_channel.send('broadcasting')

    @commands.command()
    @has_permissions(manage_guild=True)
    async def bdset(self, ctx, target_channel_name, target_guild_name = None):
        if target_guild_name is None:
            target_guild_name = ctx.guild.name
        target_channel = utils.get(self.bot.get_all_channels(), guild__name=target_guild_name, name=target_channel_name)
        if target_channel is None:
            # TODO: maybe create new channel?
            await ctx.send(f'Channel {target_channel_name} not found.')
        else:
            self.target_channel = target_channel
            await ctx.send('Suceess!')
    
    @commands.command()
    @has_permissions(manage_guild=True)
    async def bdstart(self, ctx):
        if self.target_channel is None:
            await ctx.send("Broadcast target not set!")
        else:
            self.broadcast_by_name.start()
        

async def setup(bot):
    await bot.add_cog(Broadcaster(bot))
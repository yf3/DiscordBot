from discord import utils
from discord.ext import commands
from discord.ext.commands import has_permissions
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

class Broadcaster(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.target_channel = None
        self.text_message = None
        self._default_cronexp = '*/1 * * * *'

    # @tasks.loop(seconds=1.0, count=2)
    # async def broadcast_by_name(self):
    #     await self.target_channel.send(self.text_message)

    async def broadcast_message(self):
        await self.target_channel.send(self.text_message)

    async def schedule_broadcast(self):
        scheduler = AsyncIOScheduler()
        scheduler.add_job(self.broadcast_message, CronTrigger.from_crontab(self._default_cronexp))
        scheduler.start()

    @commands.command()
    @has_permissions(manage_guild=True)
    async def bdset(self, ctx, target_channel_name, target_guild_name = None):
        if target_guild_name is None:
            target_guild_name = ctx.guild.name
        target_channel = utils.get(self.bot.get_all_channels(), guild__name=target_guild_name, name=target_channel_name)
        if target_channel is None:
            await ctx.send(f'Channel {target_channel_name} not found.')
        else:
            self.target_channel = target_channel
            await ctx.send('Suceessfully set broadcast target.')

    @commands.command()
    @has_permissions(manage_guild=True)
    async def bdtext(self, ctx, *, args):
        self.text_message = args
        if self.text_message is not None:
            await ctx.send('Successfully set broadcast message.')

    @commands.command()
    @has_permissions(manage_guild=True)
    async def bdtime(self, ctx, std_cron_expression):
        # TODO: validate cron expression
        pass

    @commands.command()
    @has_permissions(manage_guild=True)
    async def bdstart(self, ctx):
        if self.target_channel is None or self.text_message is None:
            await ctx.send("Broadcast target not set yet!")
        else:
            await self.schedule_broadcast()

async def setup(bot):
    await bot.add_cog(Broadcaster(bot))

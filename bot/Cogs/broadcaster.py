'''
Current version the bot only have one broadcast job.
'''
from discord import utils
from discord.ext import commands
from discord.ext.commands import has_permissions
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from cron_validator import CronValidator

class Broadcaster(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.target_channel = None
        self.text_message = None
        self._default_cronexp = '*/1 * * * *'
        self.custom_cronexp = None
        self.scheduler = AsyncIOScheduler()

    async def do_broadcast(self):
        await self.target_channel.send(self.text_message)

    async def schedule_broadcast(self):
        if self.custom_cronexp is None:
            cron_exp = self._default_cronexp
        else:
            cron_exp = self.custom_cronexp
        self.scheduler.add_job(self.do_broadcast, CronTrigger.from_crontab(cron_exp))
        self.scheduler.start()

    @commands.command()
    @has_permissions(manage_guild=True)
    async def bdset(self, ctx, target_channel_name, target_guild_name = None):
        if target_guild_name is None:
            target_guild_name = ctx.guild.name
        target_channel = utils.get(self.bot.get_all_channels(),
                                    guild__name=target_guild_name,
                                    name=target_channel_name)
        if target_channel is None:
            await ctx.reply(f'Channel {target_channel_name} not found.')
        else:
            self.target_channel = target_channel
            await ctx.reply('Suceessfully set broadcast target.', ephemeral=True)

    @commands.command()
    @has_permissions(manage_guild=True)
    async def bdtext(self, ctx, *, args):
        self.text_message = args
        if self.text_message is not None:
            await ctx.reply('Successfully set broadcast message.', ephemeral=True)

    @commands.command()
    @has_permissions(manage_guild=True)
    async def bdtime(self, ctx, *, cron_exp):
        try:
            CronValidator.parse(cron_exp)
            self.custom_cronexp = cron_exp
            await ctx.reply('Successfully update broadcast routine as' + cron_exp)
        except ValueError as exception:
            await ctx.reply(str(exception) +
                            '. Correct expression ref:' +
                            'https://www.ibm.com/docs/en/db2/11.5?topic=task-unix-cron-format')

    @commands.command()
    @has_permissions(manage_guild=True)
    async def bdstart(self, ctx):
        if self.target_channel is None or self.text_message is None:
            await ctx.reply('Broadcast target/message not set yet!')
        else:
            if self.scheduler.running:
                await ctx.reply('Use !bdstop to shutdown current broadcast first.')
            else:
                await self.schedule_broadcast()
    
    @commands.command()
    @has_permissions(manage_guild=True)
    async def bdstop(self, ctx):
        if self.scheduler.running:
            self.scheduler.shutdown()
            await ctx.reply('Broadcast is shutdown.')
        else:
            await ctx.reply('No running broadcast.')

async def setup(bot):
    await bot.add_cog(Broadcaster(bot))

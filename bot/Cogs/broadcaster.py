'''
Current version the bot can only have one broadcast job.
'''
from discord import utils, Embed
from discord.ext import commands
from discord.ext.commands import has_permissions
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from cron_validator import CronValidator

class Broadcaster(commands.Cog, description=
'The commands in this category requires the manage_guild permission.\n\n\
Use !bcinfo to check current settings of broadcast. Before calling \
!bcstart to start the broadcasting routine, use !bcset to \
select target channel and !bctext to set broadcast message \n\n\
Default broadcast routine is 00:00 everyday, use !bctime if you want to modify the schedule.\n\n\
If a broadcast is already running, use !bcstop then !bdstart to apply the changes.'):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.target_channel = None
        self.text_message = None
        self._default_cronexp = '0 0 * * *'
        self.custom_cronexp = None
        self.scheduler = AsyncIOScheduler()

    def _get_current_cron(self):
        if self.custom_cronexp is None:
            return self._default_cronexp
        else:
            return self.custom_cronexp

    async def do_broadcast(self):
        await self.target_channel.send(self.text_message)

    async def schedule_broadcast(self):
        cron_exp = self._get_current_cron()
        self.scheduler.add_job(self.do_broadcast, CronTrigger.from_crontab(cron_exp))
        self.scheduler.start()

    @commands.command(description='Display current broadcast settings')
    @has_permissions(manage_guild=True)
    async def bcinfo(self, ctx):
        embed = Embed(title='Current Broadcast Settings')
        embed.add_field(name='**Target Channel**', value=self.target_channel, inline=False)
        embed.add_field(name='**Cron Schedule**', value=self._get_current_cron(), inline=False)
        embed.add_field(name='**Message**', value=self.text_message, inline=False)
        embed.add_field(name='**Running**', value=self.scheduler.running)
        await ctx.reply(embed=embed)

    @commands.command(description='If target_guild_name is not given, it will choose the current guild.')
    @has_permissions(manage_guild=True)
    async def bcset(self, ctx,
                     target_channel_name: str = commands.parameter(description=' '),
                     target_guild_name: str = commands.parameter(default=None ,description='(Optional)')):
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

    @commands.command(description='Set the message you want to broadcast.')
    @has_permissions(manage_guild=True)
    async def bctext(self, ctx, *, message_content: str = commands.parameter(description=' - Any text')):
        self.text_message = message_content
        if self.text_message is not None:
            await ctx.reply('Successfully set broadcast message.', ephemeral=True)

    @commands.command(description='Set a custom schedule for the broadcast with unix cron expression.')
    @has_permissions(manage_guild=True)
    async def bctime(self, ctx, *, cron_exp):
        try:
            CronValidator.parse(cron_exp)
            self.custom_cronexp = cron_exp
            await ctx.reply('Successfully update broadcast routine as' + cron_exp)
        except ValueError as exception:
            await ctx.reply(str(exception))

    @commands.command()
    @has_permissions(manage_guild=True)
    async def bcstart(self, ctx):
        if self.target_channel is None or self.text_message is None:
            await ctx.reply('Broadcast not set yet. Use **!bcinfo** to check broadcast settings and **!help Broadcaster** for usages.')
        else:
            if self.scheduler.running:
                await ctx.reply('Use **!bcstop** to shutdown current broadcast first.')
            else:
                await self.schedule_broadcast()

    @commands.command()
    @has_permissions(manage_guild=True)
    async def bcstop(self, ctx):
        if self.scheduler.running:
            self.scheduler.shutdown()
            await ctx.reply('Broadcast is shutdown.')
        else:
            await ctx.reply('No running broadcast.')

async def setup(bot):
    await bot.add_cog(Broadcaster(bot))

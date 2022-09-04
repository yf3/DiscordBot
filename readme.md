## Bot Command Usage

Command prefix: `!` (halfwidth)

Type !help to get the full list of commands in discord:

![!help](./figs/defaultHelp.png)

### The Interaction Category

- `!echo` <message_content>
    - Making the bot reply a message to you with <message_content>.
- `!newchannel` [channel_name]
    - Add a new text channel to current guild. The channel_name will be 'new-channel' if not given.

### The Interaction Category

- `!kick` \<member\> [reason]
    - Kick out a tagged-member from current server.
    - Requires permission from the command sender.
- `!ban` \<member\> [reason]
    - Ban a tagged-member from current server.
    - Requires permission from the command sender.

### The Broadcaster category

The broadcast feature is to make the bot auto sending text message to a given channel according to a given cron expression. The commands in this category requires the manage_guild permission.

Type !help Broadcaster in channel to get the usage description from bot:

![!help Broadcast](./figs/helpBC.png)

- `!bcinfo`
    - To check current setttings of broadcast:
    ![!bcinfo](./figs/bcinfo.png)

- `!bcset` <target_channel_name> [target_guild_name]
    - To set the target channel
    - If target_guild_name is not given, it will choose the current guild.

- `!bctext` <message_content>
    - Set the message you want to broadcast.

- `!bctime` <cron_exp>
    - Set a custom schedule for the broadcast with unix cron expression.
    - This command is not required to run the broadcast if you are fine with the default schedule with cron expression `0 0 * * *` (00:00 everyday).

- `!bcstart`
    - Run the broadcast. Must setup the target channel with `!bcset` and broadcast content with `bctext` before running.

- `!bcstop`
    - Stop the current broadcast task.
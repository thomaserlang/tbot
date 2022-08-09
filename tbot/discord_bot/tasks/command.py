import logging
from discord import Permissions, Forbidden
from tbot.discord_bot import var_filler
from tbot import utils
from discord.ext import commands

class Command(commands.Cog):

    def __init__(self, bot) -> None:
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.content.startswith('!'):
            return
        args = message.content.split(' ')
        cmd = args.pop(0).lower().strip('!')

        cmds = await self.bot.db.fetchall('''
            SELECT cmd, response, enabled, roles, permissions
            FROM discord_commands
            WHERE server_id=%s AND cmd=%s AND enabled=1
        ''', (message.guild.id, cmd))
        if not cmds:
            return

        for cmd in cmds:
            try:
                roles = utils.json_loads(cmd['roles']) if cmd['roles'] else []
                if roles:
                    for r in message.author.roles:
                        if r.id in roles:
                            break
                    else:
                        return

                if cmd['permissions']:
                    if not message.author.guild_permissions.is_superset(
                        Permissions(int(cmd['permissions'], 16))
                    ):
                        return

                msg = await var_filler.fill_message(
                    cmd['response'],
                    message=message,
                    args=args,
                    bot=self.bot,
                    cmd=cmd['cmd'],
                )
                await message.channel.send(msg)
            except var_filler.Send_error as e:
                await message.channel.send('{}, {}'.format(
                    message.author.mention, 
                    str(e)
                ))        
            except var_filler.Send as e:
                await message.channel.send('{}, {}'.format(
                    message.author.mention, 
                    str(e)
                ))
            except var_filler.Send_break:
                pass
            except Forbidden as e:            
                await message.channel.send('{}, {}'.format(
                    message.author.mention, 
                    e.text
                ))
            except:
                logging.exception('command on_message')
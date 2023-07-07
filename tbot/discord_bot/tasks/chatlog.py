import json
from datetime import datetime
from discord.ext import commands
from tbot import logger
from tbot.discord_bot.custom_notification import custom_notification

class Chat_log(commands.Cog):

    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        try:
            await self.bot.db.execute('''
                INSERT INTO discord_chatlog 
                    (id, server_id, channel_id, created_at, message, 
                    attachments, user, user_id, user_discriminator, member_nick) VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            ''', (
                msg.id,
                msg.guild.id,
                msg.channel.id,
                msg.created_at,
                msg.clean_content,
                json.dumps(self.dump_attachments(msg.attachments)),
                msg.author.name,
                msg.author.id,
                msg.author.discriminator,
                msg.author.nick if hasattr(msg.author, 'nick') else None,
            ))
        except:
            logger.exception('on_message')

    @commands.Cog.listener()
    async def on_message_edit(self, before, msg):
        try:
            await self.bot.db.execute('''
                INSERT INTO discord_chatlog_versions 
                    (entry_id, created_at, message, attachments) 
                SELECT 
                    id, ifnull(updated_at, created_at), message, attachments
                FROM discord_chatlog WHERE id=%s;
            ''', (msg.id,))
            await self.bot.db.execute('''
                UPDATE discord_chatlog SET 
                    updated_at=%s, 
                    message=%s, 
                    attachments=%s
                WHERE
                    id=%s;
            ''', (
                msg.edited_at,
                msg.clean_content,
                json.dumps(self.dump_attachments(msg.attachments)),
                msg.id,
            ))
        except:
            logger.exception('on_message_edit')

    @commands.Cog.listener()
    async def on_message_delete(self, msg):
        try:
            await self.bot.db.execute('''
                UPDATE discord_chatlog SET 
                    deleted="Y",
                    deleted_at=%s
                WHERE
                    id=%s;
            ''', (datetime.utcnow(), msg.id,))
        except:
            logger.exception('on_message_delete')

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, msgs):
        try:
            f = ','.join(['%s']*len(msgs))
            await self.bot.db.execute('''
                UPDATE discord_chatlog SET 
                    deleted="Y",
                    deleted_at=%s
                WHERE
                    id IN ({});
            '''.format(f), 
                (datetime.utcnow(), *[str(m.id) for m in msgs]))
        except:
            logger.exception('on_message_delete')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            await self.bot.db.execute('''
                INSERT INTO discord_server_join_log 
                    (server_id, created_at, user, user_id, 
                    user_discriminator, member_nick, action) 
                    VALUES
                    (%s, %s, %s, %s, %s, %s, 1);
            ''', (
                member.guild.id,
                datetime.utcnow(),
                member.name,
                member.id,
                member.discriminator,
                member.nick,
            ))
        except:
            logger.exception('on_member_join')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        try:
            await self.bot.db.execute('''
                INSERT INTO discord_server_join_log 
                    (server_id, created_at, user, user_id, 
                    user_discriminator, member_nick, action) 
                    VALUES
                    (%s, %s, %s, %s, %s, %s, 0);
            ''', (
                member.guild.id,
                datetime.utcnow(),
                member.name,
                member.id,
                member.discriminator,
                member.nick,
            ))
        except:
            logger.exception('on_member_remove')

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        try:
            # Join
            if after.channel and (before.channel != after.channel):
                await self.bot.db.execute('''
                    INSERT INTO discord_voice_join_log 
                        (server_id, created_at, user, user_id, 
                        user_discriminator, member_nick, action,
                        channel_id, channel_name) 
                        VALUES
                        (%s, %s, %s, %s, %s, %s, 1, %s, %s);
                ''', (
                    member.guild.id,
                    datetime.utcnow(),
                    member.name,
                    member.id,
                    member.discriminator,
                    member.nick,
                    after.channel.id,
                    after.channel.name
                ))
                custom_notification('voice.join', after.channel.id, member.id)

            # Leave
            if before.channel and not after.channel:
                await self.bot.db.execute('''
                    INSERT INTO discord_voice_join_log 
                        (server_id, created_at, user, user_id, 
                        user_discriminator, member_nick, action,
                        channel_id, channel_name) 
                        VALUES
                        (%s, %s, %s, %s, %s, %s, 0, %s, %s);
                ''', (
                    member.guild.id,
                    datetime.utcnow(),
                    member.name,
                    member.id,
                    member.discriminator,
                    member.nick,
                    before.channel.id,
                    before.channel.name
                ))
                custom_notification('voice.leave', before.channel.id, member.id)
        except:
            logger.exception('on_voice_state_update')

    def dump_attachments(self, attachments):
        r = []
        for a in attachments:
            r.append({
                'id': a.id,
                'filename': a.filename,
                'url': a.url,
                'proxy_url': a.proxy_url,
            })
        return r
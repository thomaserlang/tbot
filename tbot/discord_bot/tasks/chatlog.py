import json, logging
from tbot.discord_bot import bot
from dateutil.parser import parse
from datetime import datetime

@bot.listen()
async def on_message(msg):
    try:
        await bot.db.execute('''
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
            json.dumps(msg.attachments),
            msg.author.name,
            msg.author.id,
            msg.author.discriminator,
            msg.author.nick,
        ))
    except:
        logging.exception('on_message')

@bot.listen()
async def on_message_edit(before, msg):
    try:
        await bot.db.execute('''
            INSERT INTO discord_chatlog_versions 
                (entry_id, created_at, message, attachments) 
            SELECT 
                id, ifnull(updated_at, created_at), message, attachments
            FROM discord_chatlog WHERE id=%s;
        ''', (msg.id,))
        await bot.db.execute('''
            UPDATE discord_chatlog SET 
                updated_at=%s, 
                message=%s, 
                attachments=%s
            WHERE
                id=%s;
        ''', (
            msg.edited_at,
            msg.clean_content,
            json.dumps(msg.attachments),
            msg.id,
        ))
    except:
        logging.exception('on_message_edit')

@bot.listen()
async def on_message_delete(msg):
    try:
        await bot.db.execute('''
            UPDATE discord_chatlog SET 
                deleted="Y",
                deleted_at=%s
            WHERE
                id=%s;
        ''', (datetime.utcnow(), msg.id,))
    except:
        logging.exception('on_message_delete')

@bot.listen()
async def on_bulk_message_delete(msgs):
    try:
        f = ','.join(['%s']*len(msgs))
        await bot.db.execute('''
            UPDATE discord_chatlog SET 
                deleted="Y",
                deleted_at=%s
            WHERE
                id IN ({});
        '''.format(f), 
            (datetime.utcnow(), *[str(m.id) for m in msgs]))
    except:
        logging.exception('on_message_delete')

@bot.listen()
async def on_member_join(member):
    try:
        await bot.db.execute('''
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
        logging.exception('on_member_join')

@bot.listen()
async def on_member_remove(member):
    try:
        await bot.db.execute('''
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
        logging.exception('on_member_remove')

@bot.listen()
async def on_voice_state_update(member, before, after):
    try:
        # Join
        if after.channel and (before.channel != after.channel):
            await bot.db.execute('''
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

        # Leave
        if before.channel and not after.channel:
            await bot.db.execute('''
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
    except:
        logging.exception('on_voice_state_update')
from tbot import config, logger
import apprise

def custom_notification(action: str, channel_id: int, member_id: int):
    if not config.data.discord.custom_notifications:
        return
    for cn in config.data.discord.custom_notifications:
        if cn.action != action:
            continue
        if cn.if_channel_ids:
            if channel_id not in cn.if_channel_ids:
                continue
        if cn.if_member_ids:
            if member_id not in cn.if_member_ids:
                continue
        try:
            apobj = apprise.Apprise()
            apobj.add(cn.apprise_dsn)
            apobj.notify(
                body=cn.message,
            )
        except Exception:
            logger.exception('custom_notification')
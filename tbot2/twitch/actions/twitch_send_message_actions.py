from ..twitch_http_client import twitch_app_client


async def twitch_send_message(
    broadcaster_id: str,
    sender_id: str,
    message: str,
    reply_parent_message_id: str | None = None,
):
    data = {
        'broadcaster_id': broadcaster_id,
        'sender_id': sender_id,
        'message': message,
    }
    if reply_parent_message_id:
        data['reply_parent_message_id'] = reply_parent_message_id

    response = await twitch_app_client.post(
        url='/chat/messages',
        json=data,
    )
    response.raise_for_status()
    return True

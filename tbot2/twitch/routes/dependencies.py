import hashlib
import hmac
from typing import Annotated

from fastapi import Depends, HTTPException, Request

from tbot2.config_settings import config

from ..schemas.eventsub_headers import EventSubHeaders


async def validate_twitch_webhook_signature(
    headers: Annotated[EventSubHeaders, Depends()],
    request: Request,
):
    message = (
        headers.message_id
        + headers.message_timestamp_raw
        + (await request.body()).decode('utf-8')
    )
    signature = (
        'sha256='
        + hmac.new(
            key=config.twitch.eventsub_secret.encode('utf-8'),
            msg=message.encode('utf-8'),
            digestmod=hashlib.sha256,
        ).hexdigest()
    )
    if headers.message_signature != signature:
        raise HTTPException(400, 'Invalid signature. What are you up to?')
    return headers

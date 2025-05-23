import asyncio
import hashlib
import hmac
from typing import Annotated

from fastapi import Depends, HTTPException, Request
from loguru import logger

from tbot2.config_settings import config
from tbot2.database import conn
from tbot2.dependecies import PlainResponse

from .schemas.event_headers_schema import EventSubHeaders
from .schemas.event_notification_schema import EventSubNotification


async def validate_twitch_webhook_signature(
    headers: Annotated[EventSubHeaders, Depends()],
    request: Request,
) -> EventSubHeaders:
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

    if headers.message_type == 'webhook_callback_verification':
        raise PlainResponse(
            status_code=200, content=(await request.json())['challenge']
        )

    if headers.message_type == 'revocation':
        revocation = EventSubNotification.model_validate_json(await request.body())  # type: ignore
        logger.info(
            f'Revocation: {revocation.subscription.type}',
            extra=revocation.subscription.condition,
        )
        raise PlainResponse(status_code=200, content='Roger')

    if headers.message_type != 'notification':
        logger.error(
            'Unknown message type: %s',
            headers.message_type,
        )
        raise PlainResponse(status_code=200, content='Roger')

    asyncio.create_task(
        conn.elasticsearch.index(
            index='twitch_events',
            document={
                'message_id': headers.message_id,
                'message_timestamp': headers.message_timestamp,
                'message_type': headers.message_type,
                'message_signature': headers.message_signature,
                'channel_id': request.query_params['channel_id'],
                **(await request.json()),
            },
        )
    )

    return headers

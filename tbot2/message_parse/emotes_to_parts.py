import asyncio
import itertools
from dataclasses import dataclass
from datetime import timedelta

from async_lru import alru_cache
from loguru import logger
from memoize.configuration import DefaultInMemoryCacheConfiguration  # type: ignore
from memoize.wrapper import memoize  # type: ignore

from tbot2.common import ChatMessagePart, EmotePart, Provider

from .http_client import http_client


@dataclass(frozen=True)
class EmotesCached:
    emotes: dict[str, EmotePart]
    emote_names: set[str]


def text_to_emote_parts(text: str, emotes: EmotesCached) -> list[ChatMessagePart]:
    parts: list[ChatMessagePart] = []
    text_buffer: list[str] = []

    def flush_text_buffer() -> None:
        if text_buffer:
            parts.append(ChatMessagePart(type='text', text=''.join(text_buffer)))
            text_buffer.clear()

    tokens = text.split(' ')
    for idx, part in enumerate(tokens):
        if part in emotes.emote_names:
            flush_text_buffer()
            parts.append(
                ChatMessagePart(type='emote', text=part, emote=emotes.emotes[part])
            )
        else:
            text_buffer.append(part)

        if idx < len(tokens) - 1:
            text_buffer.append(' ')

    # Flush any remaining text
    flush_text_buffer()
    return parts


@memoize(
    configuration=DefaultInMemoryCacheConfiguration(
        capacity=4096,
        method_timeout=timedelta(minutes=2),
        update_after=timedelta(minutes=1),
        expire_after=timedelta(minutes=10),
    )
)  # type: ignore
async def get_emotes(
    provider: Provider,
    provider_user_id: str,
) -> EmotesCached:
    results = await asyncio.gather(
        get_global_emotes(),
        get_channel_emotes(provider, provider_user_id),
    )
    emotes = {emote.name: emote for emote in itertools.chain.from_iterable(results)}
    emote_ids = set(emotes.keys())
    return EmotesCached(
        emotes=emotes,
        emote_names=emote_ids,
    )


@alru_cache(ttl=3600)
async def get_global_emotes() -> list[EmotePart]:
    results = await asyncio.gather(
        get_global_betterttv_emotes(),
        get_global_seventv_emotes(),
    )
    return list(itertools.chain.from_iterable(results))


async def get_channel_emotes(
    provider: Provider, provider_user_id: str
) -> list[EmotePart]:
    results = await asyncio.gather(
        get_channel_betterttv_emotes(provider, provider_user_id),
        get_channel_seventv_emotes(provider, provider_user_id),
    )
    return list(itertools.chain.from_iterable(results))


async def get_global_seventv_emotes() -> list[EmotePart]:
    try:
        r = await http_client.get(
            'https://7tv.io/v3/emote-sets/global',
        )
        if r.status_code > 299:
            logger.trace('Failed to get global 7tv emotes', extra={'response': r.text})
            return []
        data = r.json()['emotes']
        return [
            EmotePart(
                id=emote['data']['id'],
                name=emote['name'],
                animated=emote['data']['animated'],
                emote_provider='7tv',
            )
            for emote in data
        ]
    except Exception as e:
        logger.exception(e)
        return []


async def get_channel_seventv_emotes(
    provider: Provider, provider_user_id: str
) -> list[EmotePart]:
    try:
        r = await http_client.get(
            f'https://7tv.io/v3/users/{provider}/{provider_user_id}',
        )
        if r.status_code > 299:
            logger.trace(
                'Failed to get channel 7tv emotes',
                extra={
                    'response': r.text,
                    'provider_user_id': provider_user_id,
                    provider: provider,
                },
            )
            return []
        data = r.json()['emote_set']['emotes']
        return [
            EmotePart(
                id=emote['data']['id'],
                name=emote['name'],
                animated=emote['data']['animated'],
                emote_provider='7tv',
            )
            for emote in data
        ]
    except Exception as e:
        logger.exception(e)
        return []


async def get_global_betterttv_emotes() -> list[EmotePart]:
    try:
        r = await http_client.get(
            'https://api.betterttv.net/3/cached/emotes/global',
        )
        if r.status_code > 299:
            logger.trace('Failed to get global bttv emotes', extra={'response': r.text})
            return []
        data = r.json()
        return [
            EmotePart(
                id=emote['id'],
                name=emote['code'],
                animated=emote['animated'],
                emote_provider='bttv',
            )
            for emote in data
        ]
    except Exception as e:
        logger.exception(e)
        return []


async def get_channel_betterttv_emotes(
    provider: Provider, provider_user_id: str
) -> list[EmotePart]:
    try:
        r = await http_client.get(
            f'https://api.betterttv.net/3/cached/users/{provider}/{provider_user_id}'
        )
        if r.status_code > 299:
            logger.trace(
                'Failed to get channel bttv emotes',
                extra={
                    'response': r.text,
                    'provider_user_id': provider_user_id,
                    'provider': provider,
                },
            )
            return []
        data = r.json()
        data = data['channelEmotes'] + data['sharedEmotes']
        return [
            EmotePart(
                id=emote['id'],
                name=emote['code'],
                animated=emote['animated'],
                emote_provider='bttv',
            )
            for emote in data
        ]
    except Exception as e:
        logger.exception(e)
        return []

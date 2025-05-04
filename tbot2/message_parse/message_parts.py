
from tbot2.common import ChatMessagePart, Provider

from .emotes_to_parts import EmotesCached, get_emotes, text_to_emote_parts


async def message_to_parts(
    *,
    provider: Provider,
    provider_user_id: str,
    message: str | None = None,
    parts: list[ChatMessagePart] | None = None,
) -> list[ChatMessagePart]:
    if message is None and parts is None:
        raise ValueError('Either `message` or `parts` must be provided')
    emotes = await get_emotes(provider, provider_user_id)
    if parts is None:
        parts = [ChatMessagePart(type='text', text=message or '')]
    new_parts: list[ChatMessagePart] = []
    for part in parts:
        new_parts.extend(expand_part(part, emotes))
    return new_parts


def expand_part(part: ChatMessagePart, emotes: EmotesCached) -> list[ChatMessagePart]:
    if part.type != 'text':
        return [part]
    return text_to_emote_parts(part.text, emotes)

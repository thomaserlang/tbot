from tbot2.common import ChatMessagePartRequest, Provider

from .emotes_to_parts import EmotesCached, get_emotes, text_to_emote_parts


async def message_to_parts(
    *,
    provider: Provider,
    provider_channel_id: str,
    message: str | None = None,
    parts: list[ChatMessagePartRequest] | None = None,
) -> list[ChatMessagePartRequest]:
    if message is None and parts is None:
        raise ValueError('Either `message` or `parts` must be provided')
    emotes = await get_emotes(provider, provider_channel_id)
    if parts is None:
        parts = [ChatMessagePartRequest(type='text', text=message or '')]
    new_parts: list[ChatMessagePartRequest] = []
    for part in parts:
        new_parts.extend(expand_part(part, emotes))
    return new_parts


def expand_part(
    part: ChatMessagePartRequest, emotes: EmotesCached
) -> list[ChatMessagePartRequest]:
    if part.type != 'text':
        return [part]
    return text_to_emote_parts(part.text, emotes)

from loguru import logger

from tbot2.common import (
    ChatMessageBadge,
    ChatMessagePart,
    EmotePart,
    GiftPart,
    MentionPart,
)

from ..schemas.event_channel_chat_message_schema import (
    TwitchBadge,
    TwitchMessageFragment,
)


def twitch_badges_to_badges(
    badges: list[TwitchBadge] | None,
) -> list[ChatMessageBadge]:
    if not badges:
        return []
    return [
        ChatMessageBadge(id=badge.id, type=badge.set_id, name=badge.set_id)
        for badge in badges
    ]


def twitch_fragments_to_parts(
    fragments: list[TwitchMessageFragment],
) -> list[ChatMessagePart]:
    result: list[ChatMessagePart] = []
    for fragment in fragments:
        match fragment.type:
            case 'text':
                result.append(
                    ChatMessagePart(
                        type='text',
                        text=fragment.text,
                    )
                )
            case 'emote':
                if fragment.emote:
                    result.append(
                        ChatMessagePart(
                            type='emote',
                            text=fragment.text,
                            emote=EmotePart(
                                id=fragment.emote.id,
                                name=fragment.text,
                                animated='animated' in fragment.emote.format,
                                emote_provider='twitch',
                            ),
                        )
                    )
            case 'cheermote':
                if fragment.cheermote:
                    result.append(
                        ChatMessagePart(
                            type='gift',
                            text=fragment.text,
                            gift=GiftPart(
                                id=str(fragment.cheermote.tier),
                                name=fragment.cheermote.prefix,
                                type='cheer',
                                count=fragment.cheermote.bits,
                            ),
                        )
                    )
            case 'mention':
                if fragment.mention:
                    result.append(
                        ChatMessagePart(
                            type='mention',
                            text=fragment.text,
                            mention=MentionPart(
                                user_id=fragment.mention.user_id,
                                username=fragment.mention.user_login,
                                display_name=fragment.mention.user_name,
                            ),
                        )
                    )
            case _:
                logger.error(f'Unknown twitch fragment type: {fragment.type}')
    return result

from loguru import logger

from tbot2.common import (
    ChatMessageBadgeRequest,
    ChatMessagePartRequest,
    EmotePartRequest,
    GiftPartRequest,
    MentionPartRequest,
)

from ..schemas.event_channel_chat_message_schema import (
    TwitchBadge,
    TwitchMessageFragment,
)


def twitch_badges_to_badges(
    badges: list[TwitchBadge] | None,
) -> list[ChatMessageBadgeRequest]:
    if not badges:
        return []
    return [
        ChatMessageBadgeRequest(id=badge.id, type=badge.set_id, info=badge.info)
        for badge in badges
    ]


def twitch_fragments_to_parts(
    fragments: list[TwitchMessageFragment],
) -> list[ChatMessagePartRequest]:
    result: list[ChatMessagePartRequest] = []
    for fragment in fragments:
        match fragment.type:
            case 'text':
                result.append(
                    ChatMessagePartRequest(
                        type='text',
                        text=fragment.text,
                    )
                )
            case 'emote':
                if fragment.emote:
                    result.append(
                        ChatMessagePartRequest(
                            type='emote',
                            text=fragment.text,
                            emote=EmotePartRequest(
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
                        ChatMessagePartRequest(
                            type='gift',
                            text=fragment.text,
                            gift=GiftPartRequest(
                                id=str(fragment.cheermote.tier),
                                name=fragment.cheermote.prefix,
                                type='cheer',
                                count=fragment.cheermote.bits,
                                animated=True,
                            ),
                        )
                    )
            case 'mention':
                if fragment.mention:
                    result.append(
                        ChatMessagePartRequest(
                            type='mention',
                            text=fragment.text,
                            mention=MentionPartRequest(
                                user_id=fragment.mention.user_id,
                                username=fragment.mention.user_login,
                                display_name=fragment.mention.user_name,
                            ),
                        )
                    )
            case _:
                logger.error(f'Unknown twitch fragment type: {fragment.type}')
    return result

import random
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from uuid6 import uuid7

from tbot2.common import ChatMessageCreate

from ..actions.chat_message_actions import create_chat_message


async def seed_chat_messages(
    *, channel_id: UUID, num_messages: int = 15, session: AsyncSession | None = None
) -> None:
    usernames: list[tuple[str, str]] = [
        ('viewer1', 'Viewer One'),
        ('gamer123', 'GamerPro123'),
        ('chatfan', 'ChatFan'),
        ('streamer_friend', 'StreamerFriend'),
        ('new_user', 'NewUser'),
        ('loyal_sub', 'LoyalSubscriber'),
        ('random_chatter', 'RandomChatter'),
        ('excited_fan', 'ExcitedFan'),
        ('lurker42', 'Lurker42'),
        ('emoji_lover', 'EmojiLover😊'),
    ]

    messages: list[str] = [
        'Hello everyone!',
        'How is the stream today?',
        'LOL that was funny',
        'Great play!',
        'I love this game',
        'First time watching, this is awesome',
        'Can you explain what just happened?',
        'Followed! Great content',
        'Where are you from?',
        'GG',
        'PogChamp',
        'How long have you been streaming?',
        'Any tips for beginners?',
        'This music is great',
        'What settings do you use?',
    ]

    for _ in range(num_messages):
        username, display_name = random.choice(usernames)
        provider_channel_id = str(random.randint(10000, 99999))

        message = random.choice(messages)

        await create_chat_message(
            ChatMessageCreate(
                type='message',
                channel_id=channel_id,
                provider_viewer_id=provider_channel_id,
                viewer_name=username,
                viewer_display_name=display_name,
                provider_message_id=str(uuid7()),
                provider='twitch',
                provider_channel_id=provider_channel_id,
                message=message,
            ),
            session=session,
        )

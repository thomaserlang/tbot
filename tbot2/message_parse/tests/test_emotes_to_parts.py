from tbot2.common import ChatMessagePart, EmotePart
from tbot2.message_parse.emotes_to_parts import (
    EmotesCached,
    text_to_emote_parts,
)
from tbot2.testbase import run_file


def test_text_to_emote_parts() -> None:
    emotes = EmotesCached(
        emotes={
            'LUL': EmotePart(
                id='1',
                name='LUL',
                animated=False,
                emote_provider='twitch',
            ),
            'D:': EmotePart(
                id='2',
                name='D:',
                animated=False,
                emote_provider='twitch',
            ),
            'Kappa': EmotePart(
                id='3',
                name='Kappa',
                animated=False,
                emote_provider='twitch',
            ),
            's!': EmotePart(
                id='4',
                name='s!',
                animated=False,
                emote_provider='twitch',
            ),
        },
        emote_names={'D:', 'Kappa', 's!', 'LUL'},
    )

    r = text_to_emote_parts(
        'LUL test D:D: Kappa s! test helps! D:',
        emotes,
    )

    assert r == [
        ChatMessagePart(
            type='emote',
            text='LUL',
            emote=EmotePart(
                id='1',
                name='LUL',
                animated=False,
                emote_provider='twitch',
            ),
        ),
        ChatMessagePart(
            type='text',
            text=' test D:D: ',
        ),
        ChatMessagePart(
            type='emote',
            text='Kappa',
            emote=EmotePart(
                id='3',
                name='Kappa',
                animated=False,
                emote_provider='twitch',
            ),
        ),
        ChatMessagePart(
            type='text',
            text=' ',
        ),
        ChatMessagePart(
            type='emote',
            text='s!',
            emote=EmotePart(
                id='4',
                name='s!',
                animated=False,
                emote_provider='twitch',
            ),
        ),
        ChatMessagePart(
            type='text',
            text=' test helps! ',
        ),
        ChatMessagePart(
            type='emote',
            text='D:',
            emote=EmotePart(
                id='2',
                name='D:',
                animated=False,
                emote_provider='twitch',
            ),
        ),
    ]

    r = text_to_emote_parts(
        'LUL',
        emotes,
    )

    assert r == [
        ChatMessagePart(
            type='emote',
            text='LUL',
            emote=EmotePart(
                id='1',
                name='LUL',
                animated=False,
                emote_provider='twitch',
            ),
        ),
    ]


if __name__ == '__main__':
    run_file(__file__)

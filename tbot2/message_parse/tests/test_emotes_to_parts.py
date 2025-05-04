from tbot2.common import ChatMessagePartRequest, EmotePartRequest
from tbot2.message_parse.emotes_to_parts import (
    EmotesCached,
    text_to_emote_parts,
)
from tbot2.testbase import run_file


def test_text_to_emote_parts() -> None:
    emotes = EmotesCached(
        emotes={
            'LUL': EmotePartRequest(
                id='1',
                name='LUL',
                animated=False,
                emote_provider='twitch',
            ),
            'D:': EmotePartRequest(
                id='2',
                name='D:',
                animated=False,
                emote_provider='twitch',
            ),
            'Kappa': EmotePartRequest(
                id='3',
                name='Kappa',
                animated=False,
                emote_provider='twitch',
            ),
            's!': EmotePartRequest(
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
        ChatMessagePartRequest(
            type='emote',
            text='LUL',
            emote=EmotePartRequest(
                id='1',
                name='LUL',
                animated=False,
                emote_provider='twitch',
            ),
        ),
        ChatMessagePartRequest(
            type='text',
            text=' test D:D: ',
        ),
        ChatMessagePartRequest(
            type='emote',
            text='Kappa',
            emote=EmotePartRequest(
                id='3',
                name='Kappa',
                animated=False,
                emote_provider='twitch',
            ),
        ),
        ChatMessagePartRequest(
            type='text',
            text=' ',
        ),
        ChatMessagePartRequest(
            type='emote',
            text='s!',
            emote=EmotePartRequest(
                id='4',
                name='s!',
                animated=False,
                emote_provider='twitch',
            ),
        ),
        ChatMessagePartRequest(
            type='text',
            text=' test helps! ',
        ),
        ChatMessagePartRequest(
            type='emote',
            text='D:',
            emote=EmotePartRequest(
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
        ChatMessagePartRequest(
            type='emote',
            text='LUL',
            emote=EmotePartRequest(
                id='1',
                name='LUL',
                animated=False,
                emote_provider='twitch',
            ),
        ),
    ]


if __name__ == '__main__':
    run_file(__file__)

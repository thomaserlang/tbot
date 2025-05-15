from datetime import datetime
from typing import Literal

from tbot2.common import BaseSchema


class CheermoteImages(BaseSchema):
    dark: dict[
        Literal['animated', 'static'] | str,
        dict[Literal['1', '1.5', '2', '3', '4'] | str, str],
    ]
    'Dark theme images with animated and static formats'

    light: dict[
        Literal['animated', 'static'] | str,
        dict[Literal['1', '1.5', '2', '3', '4'] | str, str],
    ]
    'Light theme images with animated and static formats'


class CheermoteTier(BaseSchema):
    min_bits: int
    'The minimum number of Bits that you must cheer at this tier level.'

    id: str
    'The tier level.'

    color: str
    'The hex code of the color associated with this tier level.'

    images: CheermoteImages
    'The animated and static image sets for the Cheermote.'

    can_cheer: bool
    'A Boolean value that determines whether users can cheer at this tier level.'

    show_in_bits_card: bool
    'A Boolean value that determines whether this tier level is shown in the Bits card.'


class Cheermote(BaseSchema):
    prefix: str
    'The name portion of the Cheermote string that you use in chat to cheer Bits.'

    tiers: list[CheermoteTier]
    'A list of tier levels that the Cheermote supports.'

    type: (
        Literal[
            'global_first_party',
            'global_third_party',
            'channel_custom',
            'display_only',
            'sponsored',
        ]
        | str
    )
    'The type of Cheermote.'

    order: int
    'The order that the Cheermotes are shown in the Bits card.'

    last_updated: datetime
    'The date and time, in RFC3339 format, when this Cheermote was last updated.'

    is_charitable: bool
    'A Boolean value that indicates whether this Cheermote provides a charitable contribution match during charity campaigns.'  # noqa: E501


class CheermoteResponse(BaseSchema):
    data: list[Cheermote]
    "The list of Cheermotes. The list is in ascending order by the order field's value."

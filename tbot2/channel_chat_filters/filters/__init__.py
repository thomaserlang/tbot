from typing import Annotated, Union

from pydantic import Discriminator

from ..schemas.chat_filter_schema import (
    ChatFilterBase,
    ChatFilterBaseCreate,
    ChatFilterBaseUpdate,
)
from . import banned_terms_filter as banned_terms_filter
from . import caps_filter as caps_filter
from . import emote_filter as emote_filter
from . import link_filter as link_filter
from . import non_latin_filter as non_latin_filter
from . import paragraph_filter as paragraph_filter
from . import symbol_filter as symbol_filter

discriminator = Discriminator(
    'type',
    custom_error_type='type_required',
    custom_error_message='type is required',
    custom_error_context={'discriminator': 'type'},
)

FilterTypesUnion = Annotated[
    Union[tuple(ChatFilterBase.__subclasses__())], discriminator
]
FilterTypeCreateUnion = Annotated[
    Union[tuple(ChatFilterBaseCreate.__subclasses__())], discriminator
]
FilterTypeUpdateUnion = Annotated[
    Union[tuple(ChatFilterBaseUpdate.__subclasses__())], discriminator
]

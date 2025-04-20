from typing import Annotated

from pydantic import BaseModel, Field


class ContentClassificationLabel(BaseModel):
    """
    Represents a single content classification label to enable or disable.
    """

    id: Annotated[str, Field(..., description='ID of the content classification label')]
    is_enabled: Annotated[
        bool, Field(..., description='Whether this label is enabled for the channel')
    ]


class ModifyChannelInformationParams(BaseModel):
    """
    Query parameters for the Modify Channel Information request.
    """

    broadcaster_id: Annotated[
        str,
        Field(
            ...,
            description='The ID of the broadcaster whose channel you want to update',
        ),
    ]


class ModifyChannelInformationRequest(BaseModel):
    """
    Request body for the Modify Channel Information endpoint.
    All fields are optional (i.e. may be None), but at least one must be set.
    """

    game_id: Annotated[
        str | None,
        Field(
            default=None,
            description=(
                "The ID of the game that the user plays. Use '0' or '' to unset."
            ),
        ),
    ] = None
    broadcaster_language: Annotated[
        str | None,
        Field(
            default=None, description='The user’s preferred language (ISO 639‑1 code)'
        ),
    ] = None
    title: Annotated[
        str | None,
        Field(
            default=None,
            description='The title of the user’s stream (must not be empty)',
        ),
    ] = None
    delay: Annotated[
        int | None,
        Field(
            default=None, description='Stream delay in seconds (max 900; partner‑only)'
        ),
    ] = None
    tags: Annotated[
        list[str] | None,
        Field(
            default=None,
            description=(
                'A list of channel‑defined tags (max 10). '
                'Use an empty list to remove all tags.'
            ),
        ),
    ] = None
    content_classification_labels: Annotated[
        list[ContentClassificationLabel] | None,
        Field(
            default=None,
            description='List of content classification labels to add or remove',
        ),
    ] = None
    is_branded_content: Annotated[
        bool | None,
        Field(default=None, description='Whether the channel has branded content'),
    ] = None

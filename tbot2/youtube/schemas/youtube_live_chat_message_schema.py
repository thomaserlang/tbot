from datetime import datetime
from typing import Annotated, Literal

from pydantic import Field

from tbot2.common import BaseSchema


class TextMessageDetails(BaseSchema):
    message_text: Annotated[str, Field(alias='messageText')]


class MessageDeletedDetails(BaseSchema):
    deleted_message_id: Annotated[str, Field(alias='deletedMessageId')]


class BannedUserDetails(BaseSchema):
    channel_id: Annotated[str, Field(alias='channelId')]
    channel_url: Annotated[str, Field(alias='channelUrl')]
    display_name: Annotated[str, Field(alias='displayName')]
    profile_image_url: Annotated[str, Field(alias='profileImageUrl')]


class UserBannedDetails(BaseSchema):
    banned_user_details: Annotated[BannedUserDetails, Field(alias='bannedUserDetails')]
    ban_type: Annotated[str | Literal['permanent', 'temporary'], Field(alias='banType')]
    ban_duration_seconds: Annotated[int | None, Field(alias='banDurationSeconds')]


class MemberMilestoneChatDetails(BaseSchema):
    user_comment: Annotated[str, Field(alias='userComment')]
    member_month: Annotated[int, Field(alias='memberMonth')]
    member_level_name: Annotated[str, Field(alias='memberLevelName')]


class NewSponsorDetails(BaseSchema):
    member_level_name: Annotated[str, Field(alias='memberLevelName')]
    is_upgrade: Annotated[bool, Field(alias='isUpgrade')]


class SuperChatDetails(BaseSchema):
    amount_micros: Annotated[int, Field(alias='amountMicros')]
    currency: str
    amount_display_string: Annotated[str, Field(alias='amountDisplayString')]
    user_comment: Annotated[str, Field(alias='userComment')]
    tier: int


class SuperStickerMetadata(BaseSchema):
    sticker_id: Annotated[str, Field(alias='stickerId')]
    alt_text: Annotated[str, Field(alias='altText')]
    language: str


class SuperStickerDetails(BaseSchema):
    super_sticker_metadata: Annotated[
        SuperStickerMetadata, Field(alias='superStickerMetadata')
    ]
    amount_micros: Annotated[int, Field(alias='amountMicros')]
    currency: str
    amount_display_string: Annotated[str, Field(alias='amountDisplayString')]
    tier: int


class PollOption(BaseSchema):
    option_text: Annotated[str, Field(alias='optionText')]
    tally: str


class PollMetadata(BaseSchema):
    options: list[PollOption]
    question_text: Annotated[str, Field(alias='questionText')]
    status: str


class PollDetails(BaseSchema):
    metadata: PollMetadata


class MembershipGiftingDetails(BaseSchema):
    gift_memberships_count: Annotated[int, Field(alias='giftMembershipsCount')]
    gift_memberships_level_name: Annotated[str, Field(alias='giftMembershipsLevelName')]


class GiftMembershipReceivedDetails(BaseSchema):
    member_level_name: Annotated[str, Field(alias='memberLevelName')]
    gifter_channel_id: Annotated[str, Field(alias='gifterChannelId')]
    associated_membership_gifting_message_id: Annotated[
        str, Field(alias='associatedMembershipGiftingMessageId')
    ]


class Snippet(BaseSchema):
    type: (
        Literal[
            'chatEndedEvent',
            'messageDeletedEvent',
            'sponsorOnlyModeEndedEvent',
            'sponsorOnlyModeStartedEvent',
            'newSponsorEvent',
            'memberMilestoneChatEvent',
            'superChatEvent',
            'superStickerEvent',
            'textMessageEvent',
            'tombstone',
            'userBannedEvent',
            'membershipGiftingEvent',
            'giftMembershipReceivedEvent',
            'pollDetails',
        ]
        | str
    )
    live_chat_id: Annotated[str, Field(alias='liveChatId')]
    author_channel_id: Annotated[str, Field(alias='authorChannelId')]
    """
    The ID of the user that authored the message. 
    This field is only filled for the following message types:
    * If the message type is textMessageEvent, the property value identifies the user 
      that wrote the message.
    * If the message type is fanFundingEvent, the property value identifies the user 
      that funded the broadcast.
    * If the message type is messageDeletedEvent, the property value identifies the 
      moderator that deleted the message.
    * If the message type is newSponsorEvent, the property value identifies the user 
      that just became a sponsor.
    * If the message type is memberMilestoneChatEvent, the property value identifies 
      the member that sent the message.
    * If the message type is userBannedEvent, the property value identifies the 
      moderator that banned the user.
    * If the message type is membershipGiftingEvent, the property value identifies the 
      user that made the membership gifting purchase.
    * If the message type is giftMembershipReceivedEvent, the property value identifies 
      the user that received the gift membership.
    * If the message type is pollEvent, the property value identifies the user that 
      created a live poll.
    """
    published_at: Annotated[datetime, Field(alias='publishedAt')]
    has_display_content: Annotated[bool, Field(alias='hasDisplayContent')]
    display_message: Annotated[str, Field(alias='displayMessage')]
    text_message_details: Annotated[
        TextMessageDetails | None, Field(alias='textMessageDetails')
    ] = None
    message_deleted_details: Annotated[
        MessageDeletedDetails | None, Field(alias='messageDeletedDetails')
    ] = None
    user_banned_details: Annotated[
        UserBannedDetails | None, Field(alias='userBannedDetails')
    ] = None
    member_milestone_chat_details: Annotated[
        MemberMilestoneChatDetails | None, Field(alias='memberMilestoneChatDetails')
    ] = None
    new_sponsor_details: Annotated[
        NewSponsorDetails | None, Field(alias='newSponsorDetails')
    ] = None
    super_chat_details: Annotated[
        SuperChatDetails | None, Field(alias='superChatDetails')
    ] = None
    super_sticker_details: Annotated[
        SuperStickerDetails | None, Field(alias='superStickerDetails')
    ] = None
    poll_details: Annotated[PollDetails | None, Field(alias='pollDetails')] = None
    membership_gifting_details: Annotated[
        MembershipGiftingDetails | None, Field(alias='membershipGiftingDetails')
    ] = None
    gift_membership_received_details: Annotated[
        GiftMembershipReceivedDetails | None,
        Field(alias='giftMembershipReceivedDetails'),
    ] = None


class AuthorDetails(BaseSchema):
    channel_id: Annotated[str, Field(alias='channelId')]
    channel_url: Annotated[str, Field(alias='channelUrl')]
    display_name: Annotated[str, Field(alias='displayName')]
    profile_image_url: Annotated[str, Field(alias='profileImageUrl')]
    is_verified: Annotated[bool, Field(alias='isVerified')]
    is_chat_owner: Annotated[bool, Field(alias='isChatOwner')]
    is_chat_sponsor: Annotated[bool, Field(alias='isChatSponsor')]
    is_chat_moderator: Annotated[bool, Field(alias='isChatModerator')]


class LiveChatMessage(BaseSchema):
    kind: str
    etag: str
    id: str
    snippet: Snippet
    author_details: Annotated[AuthorDetails, Field(alias='authorDetails')]


class LiveChatMessages(BaseSchema):
    kind: str
    etag: str
    next_page_token: Annotated[str, Field(alias='nextPageToken')]
    polling_interval_millis: Annotated[int, Field(alias='pollingIntervalMillis')]
    offline_at: Annotated[datetime | None, Field(alias='offlineAt')] = None
    items: list[LiveChatMessage]

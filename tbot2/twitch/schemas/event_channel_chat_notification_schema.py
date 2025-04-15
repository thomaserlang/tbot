from typing import Literal

from tbot2.common import BaseSchema
from tbot2.common.schemas.twitch_schemas import TwitchBadge

from .event_channel_chat_message_schema import (
    ChannelChatMessageMessage,
)

SubTier = str | Literal['1000', '2000', '3000']


class SubNoticeMetadata(BaseSchema):
    sub_tier: SubTier
    is_prime: bool
    duration_months: int


class ResubNoticeMetadata(BaseSchema):
    cumulative_months: int
    duration_months: int
    streak_months: int
    sub_tier: SubTier
    is_prime: bool
    is_gift: bool
    gifter_is_anonymous: bool | None = None
    gifter_user_id: str | None = None
    gifter_user_name: str | None = None
    gifter_user_login: str | None = None


class SubGiftNoticeMetadata(BaseSchema):
    duration_months: int
    cumulative_total: int | None
    recipient_user_id: str
    recipient_user_name: str
    recipient_user_login: str
    sub_tier: SubTier
    community_gift_id: str | None


class CommunitySubGiftNoticeMetadata(BaseSchema):
    id: str
    total: int
    sub_tier: SubTier
    cumulative_total: int | None


class GiftPaidUpgradeNoticeMetadata(BaseSchema):
    gifter_is_anonymous: bool
    gifter_user_id: str | None
    gifter_user_name: str | None
    gifter_user_login: str | None


class PrimePaidUpgradeNoticeMetadata(BaseSchema):
    sub_tier: SubTier


class RaidNoticeMetadata(BaseSchema):
    user_id: str
    user_name: str
    user_login: str
    viewer_count: int
    profile_image_url: str


class UnraidNoticeMetadata(BaseSchema): ...


class PayItForwardNoticeMetadata(BaseSchema):
    gifter_is_anonymous: bool
    gifter_user_id: str | None
    gifter_user_name: str | None
    gifter_user_login: str | None


class AnnouncementNoticeMetadata(BaseSchema):
    color: str


class Amount(BaseSchema):
    value: int
    """The monetary amount. The amount is specified in the currency's minor unit. 
    For example, the minor units for USD is cents, so if the amount 
    is $5.50 USD, value is set to 550."""
    decimal_places: int
    """The number of decimal places used by the currency. For example, USD uses two
      decimal places. Use this number to translate value from minor 
    units to major units by using the formula: value / 10^decimal_places"""
    currency: str
    """The ISO-4217 three-letter currency code that identifies the type of 
    currency in value."""


class CharityDonationNoticeMetadata(BaseSchema):
    charity_name: str
    amount: Amount


class BitsBadgeTierNoticeMetadata(BaseSchema):
    tier: int


class EventChannelChatNotification(BaseSchema):
    broadcaster_user_id: str
    broadcaster_user_login: str
    broadcaster_user_name: str
    chatter_user_id: str
    chatter_user_login: str
    chatter_user_name: str
    chatter_is_anonymous: bool
    color: str
    badges: list[TwitchBadge]
    system_message: str
    message_id: str
    message: ChannelChatMessageMessage
    source_broadcaster_user_id: str | None
    source_broadcaster_user_login: str | None
    source_broadcaster_user_name: str | None
    source_badges: list[TwitchBadge] | None
    source_message_id: str | None

    notice_type: (
        str
        | Literal[
            'sub',
            'resub',
            'sub_gift',
            'community_sub_gift',
            'gift_paid_upgrade',
            'prime_paid_upgrade',
            'pay_it_forward',
            'raid',
            'unraid',
            'announcement',
            'bits_badge_tier',
            'charity_donation',
            'shared_chat_sub',
            'shared_chat_resub',
            'shared_chat_sub_gift',
            'shared_chat_community_sub_gift',
            'shared_chat_gift_paid_upgrade',
            'shared_chat_prime_paid_upgrade',
            'shared_chat_pay_it_forward',
            'shared_chat_raid',
            'shared_chat_announcement',
        ]
    )
    sub: SubNoticeMetadata | None
    resub: ResubNoticeMetadata | None
    sub_gift: SubGiftNoticeMetadata | None
    community_sub_gift: CommunitySubGiftNoticeMetadata | None
    gift_paid_upgrade: GiftPaidUpgradeNoticeMetadata | None
    prime_paid_upgrade: PrimePaidUpgradeNoticeMetadata | None
    raid: RaidNoticeMetadata | None
    unraid: UnraidNoticeMetadata | None
    pay_it_forward: PayItForwardNoticeMetadata | None
    announcement: AnnouncementNoticeMetadata | None
    bits_badge_tier: BitsBadgeTierNoticeMetadata | None
    charity_donation: CharityDonationNoticeMetadata | None
    shared_chat_sub: SubNoticeMetadata | None
    shared_chat_resub: ResubNoticeMetadata | None
    shared_chat_sub_gift: SubGiftNoticeMetadata | None
    shared_chat_community_sub_gift: CommunitySubGiftNoticeMetadata | None
    shared_chat_gift_paid_upgrade: GiftPaidUpgradeNoticeMetadata | None
    shared_chat_prime_paid_upgrade: PrimePaidUpgradeNoticeMetadata | None
    shared_chat_pay_it_forward: PayItForwardNoticeMetadata | None
    shared_chat_raid: RaidNoticeMetadata | None
    shared_chat_announcement: AnnouncementNoticeMetadata | None

from typing import Literal

ChatMessageType = Literal['message', 'notice', 'status']

TwitchNoticeType = Literal[
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
    'cheer',  # custom added
]

TwitchModerateAction = Literal[
    'ban',
    'timeout',
    'unban',
    'untimeout',
    'clear',
    'emoteonly',
    'emoteonlyoff',
    'followers',
    'followersoff',
    'uniquechat',
    'uniquechatoff',
    'slow',
    'slowoff',
    'subscribers',
    'subscribersoff',
    'unraid',
    'delete',
    'vip',
    'unvip',
    'raid',
    'add_blocked_term',
    'add_permitted_term',
    'remove_blocked_term',
    'remove_permitted_term',
    'mod',
    'unmod',
    'approve_unban_request',
    'deny_unban_request',
    'warn',
]

TwitchChatMessageType = Literal[
    'text',
    'custom_reward_redemption',
    'channel_points_highlighted',
    'channel_points_sub_only',
    'user_intro',
    'power_ups_message_effect',
    'power_ups_gigantified_emote',
]

YoutubeNoticeType = Literal[
    'newSponsorEvent',
    'superChatEvent',
    'superStickerEvent',
    'membershipGiftingEvent',
    'giftMembershipReceivedEvent',
]

YoutubeMessageType = (
    Literal[
        'chatEndedEvent',
        'messageDeletedEvent',
        'sponsorOnlyModeEndedEvent',
        'sponsorOnlyModeStartedEvent',
        'memberMilestoneChatEvent',
        'textMessageEvent',
        'tombstone',
        'userBannedEvent',
        'pollDetails',
    ]
    | YoutubeNoticeType
)

TiktokNoticeType = Literal['gift']

ChatMessageSubType = (
    TwitchNoticeType
    | TwitchModerateAction
    | TwitchChatMessageType
    | YoutubeMessageType
    | TiktokNoticeType
)

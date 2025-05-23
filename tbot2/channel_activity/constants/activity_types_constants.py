from ..types.activity_type import ActivityTypeName

TWITCH_ACTIVITY_TYPE_NAMES: list[ActivityTypeName] = [
    ActivityTypeName(
        name='sub',
        display_name='New Sub',
        color='#EFBF04',  # Gold
        filter_min_count=False,
        provider='twitch',
        count_name='months',
        sub_type_names={
            'prime': 'Prime',
            '1000': 'T1',
            '2000': 'T2',
            '3000': 'T3',
        },
    ),
    ActivityTypeName(
        name='resub',
        display_name='Resub',
        color='#EFBF04',  # Gold
        filter_min_count=False,
        provider='twitch',
        count_name='months',
        sub_type_names={
            'prime': 'Prime',
            '1000': 'T1',
            '2000': 'T2',
            '3000': 'T3',
        },
    ),
    ActivityTypeName(
        name='gift_sub',
        display_name='Gift Sub',
        color='#F9A825',  # Warm amber gold
        filter_min_count=False,
        provider='twitch',
        count_name='months',
        sub_type_names={
            'prime': 'Prime',
            '1000': 'T1',
            '2000': 'T2',
            '3000': 'T3',
        },
    ),
    ActivityTypeName(
        name='community_sub_gift',
        display_name='Gift subs',
        color='#FFC107',  # Golden amber
        filter_min_count=True,
        provider='twitch',
        count_name='subs',
        sub_type_names={
            'prime': 'Prime',
            '1000': 'T1',
            '2000': 'T2',
            '3000': 'T3',
        },
    ),
    ActivityTypeName(
        name='raid',
        display_name='Raid',
        color='#FF5252',  # Vibrant red
        filter_min_count=True,
        provider='twitch',
        count_name='raiders',
    ),
    ActivityTypeName(
        name='charity_donation',
        display_name='Charity Donation',
        color='#4CAF50',  # Rich green
        filter_min_count=True,
        provider='twitch',
        count_name='',
    ),
    ActivityTypeName(
        name='bits',
        display_name='Bits',
        color='#00BCD4',  # Cyan blue
        filter_min_count=True,
        provider='twitch',
        count_name='bits',
    ),
    ActivityTypeName(
        name='follow',
        display_name='Follow',
        color='#8BC34A',  # Light green
        provider='twitch',
        count_name='',
    ),
    ActivityTypeName(
        name='points',
        display_name='Points',
        color='#9E9E9E',  # Gray
        filter_min_count=True,
        provider='twitch',
        count_name='points',
    ),
]

YOUTUBE_ACTIVITY_TYPE_NAMES: list[ActivityTypeName] = [
    ActivityTypeName(
        name='newSponsorEvent',
        display_name='New Member',
        color='#FF0000',  # YouTube red
        filter_min_count=False,
        provider='youtube',
        count_name='',
    ),
    ActivityTypeName(
        name='superChatEvent',
        display_name='SuperChat',
        color='#2196F3',  # Bright blue
        filter_min_count=True,
        provider='youtube',
        count_name='',
    ),
    ActivityTypeName(
        name='superStickerEvent',
        display_name='SuperSticker',
        color='#FFC107',  # Gold
        filter_min_count=True,
        provider='youtube',
        count_name='',
    ),
    ActivityTypeName(
        name='membershipGiftingEvent',
        display_name='MemberGifting',
        color='#4CAF50',  # Rich green
        filter_min_count=True,
        provider='youtube',
        count_name='memberships',
    ),
    ActivityTypeName(
        name='memberMilestoneChatEvent',
        display_name='MemberMilestone',
        color='#9C27B0',  # Rich purple
        filter_min_count=False,
        provider='youtube',
        count_name='months',
    ),
]

TIKTOK_ACTIVITY_TYPE_NAMES: list[ActivityTypeName] = [
    ActivityTypeName(
        name='gift',
        display_name='Gift',
        color='#FE2C55',  # TikTok pink
        filter_min_count=True,
        provider='tiktok',
        count_name='dia',
    ),
]

ACTIVITY_TYPE_NAMES: list[ActivityTypeName] = (
    TWITCH_ACTIVITY_TYPE_NAMES
    + YOUTUBE_ACTIVITY_TYPE_NAMES
    + TIKTOK_ACTIVITY_TYPE_NAMES
)

ACTIVITY_TYPE_NAMES_DICT = {
    activity_type.name: activity_type for activity_type in ACTIVITY_TYPE_NAMES
}

from tbot2.common import BaseSchema


class CustomRewardImage(BaseSchema):
    url_1x: str
    """The URL to a small version of the image."""
    url_2x: str
    """The URL to a medium version of the image."""
    url_4x: str
    """The URL to a large version of the image."""


class CustomRewardMaxPerStreamSetting(BaseSchema):
    is_enabled: bool
    """A Boolean value that determines whether the reward applies a limit on the number of redemptions allowed per live stream. Is true if the reward applies a limit."""  # noqa: E501
    max_per_stream: int
    """The maximum number of redemptions allowed per live stream."""


class CustomRewardMaxPerUserPerStreamSetting(BaseSchema):
    is_enabled: bool
    """A Boolean value that determines whether the reward applies a limit on the number of redemptions allowed per user per live stream. Is true if the reward applies a limit."""  # noqa: E501
    max_per_user_per_stream: int
    """The maximum number of redemptions allowed per user per live stream."""


class CustomRewardGlobalCooldownSetting(BaseSchema):
    is_enabled: bool
    """A Boolean value that determines whether to apply a cooldown period. Is true if a cooldown period is enabled."""  # noqa: E501
    global_cooldown_seconds: int
    """The cooldown period, in seconds."""


class CustomReward(BaseSchema):
    broadcaster_id: str
    """The ID that uniquely identifies the broadcaster."""
    broadcaster_login: str
    """The broadcaster's login name."""
    broadcaster_name: str
    """The broadcaster's display name."""
    id: str
    """The ID that uniquely identifies this custom reward."""
    title: str
    """The title of the reward."""
    prompt: str
    """The prompt shown to the viewer when they redeem the reward if user input is required (see the is_user_input_required field)."""  # noqa: E501
    cost: int
    """The cost of the reward in Channel Points."""
    image: CustomRewardImage | None
    """A set of custom images for the reward. This field is null if the broadcaster didn't upload images."""  # noqa: E501
    default_image: CustomRewardImage
    """A set of default images for the reward."""
    background_color: str
    """The background color to use for the reward. The color is in Hex format (for example, #00E5CB)."""  # noqa: E501
    is_enabled: bool
    """A Boolean value that determines whether the reward is enabled. Is true if enabled; otherwise, false. Disabled rewards aren't shown to the user."""  # noqa: E501
    is_user_input_required: bool
    """A Boolean value that determines whether the user must enter information when redeeming the reward. Is true if the user is prompted."""  # noqa: E501
    max_per_stream_setting: CustomRewardMaxPerStreamSetting
    """The settings used to determine whether to apply a maximum to the number of redemptions allowed per live stream."""  # noqa: E501
    max_per_user_per_stream_setting: CustomRewardMaxPerUserPerStreamSetting
    """The settings used to determine whether to apply a maximum to the number of redemptions allowed per user per live stream."""  # noqa: E501
    global_cooldown_setting: CustomRewardGlobalCooldownSetting
    """The settings used to determine whether to apply a cooldown period between redemptions and the length of the cooldown."""  # noqa: E501
    is_paused: bool
    """A Boolean value that determines whether the reward is currently paused. Is true if the reward is paused. Viewers can't redeem paused rewards."""  # noqa: E501
    is_in_stock: bool
    """A Boolean value that determines whether the reward is currently in stock. Is true if the reward is in stock. Viewers can't redeem out of stock rewards."""  # noqa: E501
    should_redemptions_skip_request_queue: bool
    """A Boolean value that determines whether redemptions should be set to FULFILLED status immediately when a reward is redeemed. If false, status is set to UNFULFILLED and follows the normal request queue process."""  # noqa: E501
    redemptions_redeemed_current_stream: int | None
    """The number of redemptions redeemed during the current live stream. The number counts against the max_per_stream_setting limit. This field is null if the broadcaster's stream isn't live or max_per_stream_setting isn't enabled."""  # noqa: E501
    cooldown_expires_at: str | None
    """The timestamp of when the cooldown period expires. Is null if the reward isn't in a cooldown state. See the global_cooldown_setting field."""  # noqa: E501


class CustomRewardResponse(BaseSchema):
    data: list[CustomReward]
    """A list of custom rewards. The list is in ascending order by id. If the broadcaster hasn't created custom rewards, the list is empty."""  # noqa: E501

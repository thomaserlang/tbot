from .types.feature_type import Feature
from .types.subscription_type import SubscriptionType

TBOT_CHANNEL_ID_HEADER = 'X-TBot-Channel-Id'
APP_TITLE = 'Synchra'

FEATURES_BY_SUBSCRIPTION: dict[SubscriptionType, set[Feature]] = {
    SubscriptionType.PRO_PLUS: {
        Feature.CHANNEL_VIEWER_EXTRA_STATS,
    }
}

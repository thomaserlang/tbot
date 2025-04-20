from tbot2.channel import ChannelProvider, on_event_update_stream_title

from ..actions.youtube_live_broadcast_actions import update_live_broadcast


@on_event_update_stream_title('youtube')
async def update_stream_title(
    channel_provider: ChannelProvider,
    stream_title: str,
) -> bool:
    await update_live_broadcast(
        channel_provider=channel_provider,
        snippet_title=stream_title[:100],
    )
    return True

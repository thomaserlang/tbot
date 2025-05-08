from uuid import UUID

from tbot2.channel_queue import (
    Queue,
    QueueViewerCreate,
    create_queue_viewer,
    get_queue_viewer_by_provider,
    get_queues,
)
from tbot2.common import ChatMessageRequest

from ..exceptions import CommandError
from ..types import MessageVars, TCommand
from ..var_filler import fills_vars


@fills_vars(provider='all', vars=('queue_join', 'queue_join.position'))
async def queue_join_vars(
    chat_message: ChatMessageRequest, command: TCommand, vars: MessageVars
) -> None:
    queue = await get_queue(
        chat_message.channel_id,
        name=' '.join(vars['queue_join'].args)
        or ' '.join(vars['queue_join.position'].args),
    )

    viewer = await get_queue_viewer_by_provider(
        channel_queue_id=queue.id,
        provider=chat_message.provider,
        provider_viewer_id=chat_message.provider_viewer_id,
    )
    if viewer:
        raise CommandError(
            f'You are already in the queue at position {viewer.position}'
        )

    viewer = await create_queue_viewer(
        channel_queue_id=queue.id,
        data=QueueViewerCreate(
            provider=chat_message.provider,
            provider_viewer_id=chat_message.provider_viewer_id,
            display_name=chat_message.viewer_display_name,
        ),
    )
    vars['queue_join'].value = ''
    vars['queue_join.position'].value = viewer.position


@fills_vars(provider='all', vars=('queue.position',))
async def queue_position_vars(
    chat_message: ChatMessageRequest, command: TCommand, vars: MessageVars
) -> None:
    queue = await get_queue(
        chat_message.channel_id, name=' '.join(vars['queue.position'].args)
    )
    viewer = await get_queue_viewer_by_provider(
        channel_queue_id=queue.id,
        provider=chat_message.provider,
        provider_viewer_id=chat_message.provider_viewer_id,
    )
    if not viewer:
        raise CommandError('You are not in the queue')
    vars['queue.position'].value = viewer.position


@fills_vars(provider='all', vars=('queue.leave',))
async def queue_leave_vars(
    chat_message: ChatMessageRequest, command: TCommand, vars: MessageVars
) -> None:
    queue = await get_queue(
        chat_message.channel_id, name=' '.join(vars['queue.leave'].args)
    )
    viewer = await get_queue_viewer_by_provider(
        channel_queue_id=queue.id,
        provider=chat_message.provider,
        provider_viewer_id=chat_message.provider_viewer_id,
    )
    if not viewer:
        raise CommandError('You are not in the queue.')
    vars['queue.leave'].value = ''


async def get_queue(
    channel_id: UUID,
    name: str | None = None,
) -> Queue:
    queues = await get_queues(channel_id=channel_id, name=name)
    if not queues:
        raise CommandError('Found no queue. Create one in the dashboard.')
    return queues[0]

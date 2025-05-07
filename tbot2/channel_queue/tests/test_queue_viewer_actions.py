import pytest

from tbot2.channel_queue import (
    QueueCreate,
    QueueViewerCreate,
    add_viewer_to_queue,
    clear_queue,
    create_queue,
    get_queue_viewer_by_provider,
    move_viewer_to_top,
    remove_viewer_from_queue,
)
from tbot2.common import ErrorMessage
from tbot2.testbase import run_file, user_signin


@pytest.mark.asyncio
async def test_queue_viewer_actions(db: None) -> None:
    user = await user_signin(client=None, scopes=[])

    queue = await create_queue(
        channel_id=user.channel.id,
        data=QueueCreate(
            name='Test queue',
        ),
    )

    viewer_item = await add_viewer_to_queue(
        channel_queue_id=queue.id,
        data=QueueViewerCreate(
            provider='twitch',
            provider_viewer_id='test1',
            display_name='test1',
        ),
    )
    assert viewer_item.id is not None
    assert viewer_item.channel_queue_id == queue.id
    assert viewer_item.provider == 'twitch'
    assert viewer_item.provider_viewer_id == 'test1'
    assert viewer_item.display_name == 'test1'
    assert viewer_item.position == 1

    # Test adding the same viewer again
    with pytest.raises(ErrorMessage) as excinfo:
        await add_viewer_to_queue(
            channel_queue_id=queue.id,
            data=QueueViewerCreate(
                provider='twitch',
                provider_viewer_id='test1',
                display_name='test1',
            ),
        )
    assert str(excinfo.value) == 'Viewer already in queue'

    # Test adding a different viewer
    viewer_item2 = await add_viewer_to_queue(
        channel_queue_id=queue.id,
        data=QueueViewerCreate(
            provider='twitch',
            provider_viewer_id='test2',
            display_name='test2',
        ),
    )
    assert viewer_item2.id is not None
    assert viewer_item2.channel_queue_id == queue.id
    assert viewer_item2.provider == 'twitch'
    assert viewer_item2.provider_viewer_id == 'test2'
    assert viewer_item2.display_name == 'test2'
    assert viewer_item2.position == 2

    viewer_item3 = await add_viewer_to_queue(
        channel_queue_id=queue.id,
        data=QueueViewerCreate(
            provider='twitch',
            provider_viewer_id='test3',
            display_name='test3',
        ),
    )
    assert viewer_item3.id is not None
    assert viewer_item3.channel_queue_id == queue.id
    assert viewer_item3.provider == 'twitch'
    assert viewer_item3.provider_viewer_id == 'test3'
    assert viewer_item3.display_name == 'test3'
    assert viewer_item3.position == 3

    # Test moving a viewer to the top
    await move_viewer_to_top(
        channel_queue_viewer_id=viewer_item2.id,
    )

    viewer_item = await get_queue_viewer_by_provider(
        channel_queue_id=queue.id,
        provider='twitch',
        provider_viewer_id='test2',
    )
    assert viewer_item
    assert viewer_item.position == 1

    viewer_item1 = await get_queue_viewer_by_provider(
        channel_queue_id=queue.id,
        provider='twitch',
        provider_viewer_id='test1',
    )
    assert viewer_item1
    assert viewer_item1.position == 2

    viewer_item = await get_queue_viewer_by_provider(
        channel_queue_id=queue.id,
        provider='twitch',
        provider_viewer_id='test3',
    )
    assert viewer_item
    assert viewer_item.position == 3

    await remove_viewer_from_queue(
        channel_queue_viewer_id=viewer_item1.id,
    )

    viewer_item = await get_queue_viewer_by_provider(
        channel_queue_id=queue.id,
        provider='twitch',
        provider_viewer_id='test3',
    )
    assert viewer_item
    assert viewer_item.position == 2

    viewer_item = await get_queue_viewer_by_provider(
        channel_queue_id=queue.id,
        provider='twitch',
        provider_viewer_id='test2',
    )
    assert viewer_item
    assert viewer_item.position == 1

    await clear_queue(
        channel_queue_id=queue.id,
    )
    viewer_item = await get_queue_viewer_by_provider(
        channel_queue_id=queue.id,
        provider='twitch',
        provider_viewer_id='test3',
    )
    assert viewer_item is None
    viewer_item = await get_queue_viewer_by_provider(
        channel_queue_id=queue.id,
        provider='twitch',
        provider_viewer_id='test2',
    )
    assert viewer_item is None


if __name__ == '__main__':
    run_file(__file__)

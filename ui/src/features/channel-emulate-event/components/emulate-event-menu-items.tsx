import { useCurrentChannel } from '@/features/channel'
import { toastPromise } from '@/utils/toast'
import { Menu } from '@mantine/core'
import { emulateEvents } from '../constants'

export function EmulateEventMenuItems() {
    const channel = useCurrentChannel()

    return (
        <>
            {emulateEvents.map((event) => (
                <Menu.Item
                    key={event.name}
                    variant="default"
                    onClick={() => {
                        toastPromise({
                            promise: event.request({
                                channelId: channel.id,
                            }),
                            loading: {
                                title: `Emulating ${event.name}...`,
                            },
                            success: { title: `${event.name} emulated` },
                            error: {
                                title: `Failed to emulate ${event.name}`,
                            },
                        })
                    }}
                >
                    {event.name}
                </Menu.Item>
            ))}
        </>
    )
}

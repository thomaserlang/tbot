import { toastPromise } from '@/utils/toast'
import { ActionIcon, Menu, MenuItem } from '@mantine/core'
import { IconDotsVertical, IconEdit, IconTrash } from '@tabler/icons-react'
import { useDeleteTimer } from '../timer.api'
import { Timer } from '../timer.types'

interface Props {
    timer: Timer
    onEditClick?: (Timer: Timer) => void
    onDeleted?: (Timer: Timer) => void
}

export function TimerMenu({ timer, onEditClick }: Props) {
    const deleteTimer = useDeleteTimer()

    return (
        <Menu width={200}>
            <Menu.Target>
                <ActionIcon variant="subtle" color="gray">
                    <IconDotsVertical size={16} />
                </ActionIcon>
            </Menu.Target>

            <Menu.Dropdown>
                <MenuItem
                    leftSection={<IconEdit size={14} />}
                    onClick={() => onEditClick?.(timer)}
                >
                    Edit
                </MenuItem>
                <Menu.Item
                    color="red"
                    leftSection={<IconTrash size={14} />}
                    onClick={() => {
                        toastPromise({
                            promise: deleteTimer.mutateAsync({
                                timerId: timer.id,
                                channelId: timer.channel_id,
                            }),
                            loading: {
                                title: 'Deleting Timer',
                            },
                            success: {
                                title: 'Timer deleted',
                            },
                            error: {
                                title: 'Failed to delete Timer',
                            },
                        })
                    }}
                >
                    Delete
                </Menu.Item>
            </Menu.Dropdown>
        </Menu>
    )
}

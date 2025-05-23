import { ChannelId } from '@/features/channel'
import { toastPromise } from '@/utils/toast'
import { Menu } from '@mantine/core'
import { openConfirmModal } from '@mantine/modals'
import { IconTrash } from '@tabler/icons-react'
import { deleteActivity } from '../api/activity.api'
import { ActivityId } from '../types/activity.type'

interface Props {
    channelId: ChannelId
    activityId: ActivityId
    children: React.ReactElement
}

export function ActivityItemMenu({ children, channelId, activityId }: Props) {
    return (
        <Menu width={200}>
            <Menu.Target>{children}</Menu.Target>

            <Menu.Dropdown>
                <Menu.Item
                    leftSection={<IconTrash size={16} />}
                    color="red"
                    onClick={() => {
                        openConfirmModal({
                            title: 'Delete activity',
                            children: (
                                <>
                                    <p>
                                        Are you sure you want to delete this
                                        activity?
                                    </p>
                                    <p>This action cannot be undone.</p>
                                </>
                            ),
                            labels: {
                                confirm: 'Delete activity',
                                cancel: 'Cancel',
                            },
                            confirmProps: { color: 'red' },
                            onConfirm: () => {
                                toastPromise({
                                    promise: deleteActivity({
                                        channelId,
                                        activityId,
                                    }),
                                    loading: {
                                        title: 'Deleting activity',
                                    },
                                    success: {
                                        title: 'Activity deleted',
                                    },
                                    error: {
                                        title: 'Error deleting activity',
                                    },
                                })
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

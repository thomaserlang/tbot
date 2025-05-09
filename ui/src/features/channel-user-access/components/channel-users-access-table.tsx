import { ErrorBox } from '@/components/error-box'
import { accessLevelInfo } from '@/constants/access-levels-info.constants'
import { ChannelId } from '@/features/channel/types/channel.types'
import { pageRecordsFlatten } from '@/utils/page-records'
import { toastPromise } from '@/utils/toast'
import { ActionIcon, Group, Text } from '@mantine/core'
import { openConfirmModal } from '@mantine/modals'
import { IconX } from '@tabler/icons-react'
import { DataTable } from 'mantine-datatable'
import {
    useDeleteChannelUserAccess,
    useGetChannelUsersAccess,
} from '../api/channel-user-access.api'
import { ChannelUserAccess } from '../types/channel-user-access.types'

interface Props {
    channelId: ChannelId
}

export function ChannelUsersAccessTable({ channelId }: Props) {
    const { data, isLoading, error } = useGetChannelUsersAccess({ channelId })
    const deleteUserAccess = useDeleteChannelUserAccess()

    if (error) return <ErrorBox errorObj={error} />

    const deleteUserAccessModal = (channelUserAccess: ChannelUserAccess) => {
        openConfirmModal({
            title: 'Remove user access',
            children: (
                <Text>
                    Are you sure you want to remove{' '}
                    {channelUserAccess.user.display_name}'s access?
                </Text>
            ),
            labels: { confirm: 'Remove', cancel: 'Cancel' },
            confirmProps: { color: 'red' },
            onConfirm: () => {
                toastPromise({
                    promise: deleteUserAccess.mutateAsync({
                        channelId,
                        channelUserAccessId: channelUserAccess.id,
                    }),
                    loading: {
                        title: 'Removing user access',
                    },
                    success: {
                        title: 'User access removed',
                    },
                    error: {
                        title: 'Error removing user access',
                    },
                })
            },
        })
    }

    const records = pageRecordsFlatten(data)

    return (
        <DataTable
            withTableBorder
            highlightOnHover
            records={records}
            noRecordsText="No users with access"
            fetching={isLoading}
            minHeight={records.length ? 0 : 150}
            columns={[
                { accessor: 'user.display_name', title: 'Name' },
                {
                    accessor: 'access_level',
                    title: 'Access Level',
                    render: (item) => {
                        return (
                            accessLevelInfo?.[item.access_level].label ??
                            item.access_level
                        )
                    },
                },
                {
                    accessor: '',
                    title: '',
                    width: '1%',
                    render: (item) => (
                        <Group>
                            <ActionIcon
                                size="sm"
                                color="red"
                                variant="subtle"
                                title="Remove user access"
                                onClick={() => {
                                    deleteUserAccessModal(item)
                                }}
                            >
                                <IconX size={20} />
                            </ActionIcon>
                        </Group>
                    ),
                },
            ]}
        />
    )
}

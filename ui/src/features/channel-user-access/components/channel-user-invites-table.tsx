import { ErrorBox } from '@/components/error-box'
import { RelativeTimeUpdater } from '@/components/relative-time-updater'
import { accessLevelInfo } from '@/constants/access-levels-info.constants'
import { ChannelId } from '@/features/channel/types/channel.types'
import { pageRecordsFlatten } from '@/utils/page-records'
import { toastPromise } from '@/utils/toast'
import { ActionIcon, Group, Text } from '@mantine/core'
import { openConfirmModal } from '@mantine/modals'
import { IconX } from '@tabler/icons-react'
import { DataTable } from 'mantine-datatable'
import {
    useDeleteChannelUserInvite,
    useGetChannelUserInvites,
} from '../api/channel-user-invite.api'
import { ChannelUserInvite } from '../types/channel-user-invite.types'

interface Props {
    channelId: ChannelId
}

export function ChannelUserInvitesTable({ channelId }: Props) {
    const { data, isLoading, error } = useGetChannelUserInvites({ channelId })
    const deleteUserInvite = useDeleteChannelUserInvite()

    if (error) return <ErrorBox errorObj={error} />

    const deleteUserInviteModal = (channelUserInvite: ChannelUserInvite) => {
        openConfirmModal({
            title: 'Remove user access',
            children: <Text>Delete invite?</Text>,
            labels: { confirm: 'Delete', cancel: 'Cancel' },
            confirmProps: { color: 'red' },
            onConfirm: () => {
                toastPromise({
                    promise: deleteUserInvite.mutateAsync({
                        channelId,
                        channelUserInviteId: channelUserInvite.id,
                    }),
                    loading: {
                        title: 'Removing user invite',
                    },
                    success: {
                        title: 'User invite removed',
                    },
                    error: {
                        title: 'Error removing user invite',
                    },
                })
            },
        })
    }

    const records = pageRecordsFlatten(data)

    return (
        <DataTable
            withTableBorder
            noHeader
            records={records}
            minHeight={records.length > 0 ? 0 : 150}
            noRecordsText="No invite links"
            fetching={isLoading}
            columns={[
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
                    accessor: 'expired',
                    title: 'Expires At',
                    render: (item) => {
                        return item.expired ? (
                            'Expired'
                        ) : (
                            <>
                                Expires{' '}
                                <RelativeTimeUpdater dt={item.expires_at} />
                            </>
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
                                title="Delete user invite"
                                onClick={() => {
                                    deleteUserInviteModal(item)
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

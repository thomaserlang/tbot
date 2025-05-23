import { useCurrentUserSettings } from '@/components/current-user/current-user-settings.provider'
import { ErrorBox } from '@/components/error-box'
import { PageLoader } from '@/components/page-loader'
import { ShortRelativeTimeUpdater } from '@/components/relative-time-updater'
import { ChannelId } from '@/features/channel'
import { pageRecordsFlatten } from '@/utils/page-records'
import { toastPromise } from '@/utils/toast'
import { Flex, Text } from '@mantine/core'
import { openConfirmModal } from '@mantine/modals'
import { IconActivity, IconTrash } from '@tabler/icons-react'
import { useContextMenu } from 'mantine-contextmenu'
import { DataTable } from 'mantine-datatable'
import { useState } from 'react'
import { useGetActivities, useWSActivities } from '../api/activities.api'
import { deleteActivity, useUpdateActivity } from '../api/activity.api'
import { ActivityId } from '../types/activity.type'
import { InfoColumn } from './info-column'

interface Props {
    channelId: ChannelId
}

export function ActivityFeedTable({ channelId }: Props) {
    const { settings } = useCurrentUserSettings()
    const update = useUpdateActivity()
    const minCounts = Object.entries(
        settings.activity_feed_type_min_count
    ).reduce((acc, [key, value]) => {
        if (value > 0) {
            acc.push(`${key}.${value}`)
        }
        return acc
    }, [] as string[])
    const data = useGetActivities({
        channelId,
        params: {
            not_type: settings.activity_feed_not_types,
            min_count: minCounts,
        },
    })
    useWSActivities({
        channelId,
        params: {
            not_type: settings.activity_feed_not_types,
            min_count: minCounts,
        },
    })
    const { showContextMenu } = useContextMenu()
    const [selected, setSelected] = useState<ActivityId | null>(null)

    const size = 'sm'

    if (data.isLoading) return <PageLoader />
    if (!data.data && data.error) return <ErrorBox errorObj={data.error} />

    const activities = pageRecordsFlatten(data.data)

    return (
        <DataTable
            records={activities}
            noRecordsText="No activity"
            noRecordsIcon={<IconActivity />}
            noHeader
            highlightOnHover
            pinLastColumn
            pinFirstColumn
            onScrollToBottom={data.fetchNextPage}
            verticalSpacing="xs"
            onRowClick={({ record }) => {
                setSelected(record.id === selected ? null : record.id)

                update.mutate({
                    channelId,
                    activityId: record.id,
                    data: { read: !record.read },
                })
            }}
            rowBackgroundColor={(record) =>
                record.id === selected ? 'var(--tbot-selected-color)' : ''
            }
            columns={[
                {
                    accessor: 'read',
                    noWrap: true,
                    width: '0.25rem',
                    hidden: !settings.activity_feed_read_indicator,
                    render: (activity) => (
                        <div
                            style={{
                                width: '0.25rem',
                                height: '1rem',
                                backgroundColor: activity.read
                                    ? ''
                                    : 'var(--mantine-color-grape-6)',
                            }}
                        />
                    ),
                    cellsStyle: () => ({
                        padding: 0,
                    }),
                },
                {
                    accessor: 'type_display_name',
                    noWrap: true,
                    width: '1%',
                    render: (activity) => (
                        <InfoColumn activity={activity} size={size} />
                    ),
                },
                {
                    accessor: 'message',
                    noWrap: true,
                    render: (activity) => (
                        <Text
                            size={size}
                            c="dimmed"
                            title={activity.message || ''}
                        >
                            {activity.message}
                        </Text>
                    ),
                },
                {
                    accessor: 'created_at',
                    textAlign: 'right',
                    noWrap: true,

                    render: (activity) => (
                        <Flex gap="0.25rem" align="center">
                            <Text size={size} c="dimmed">
                                <ShortRelativeTimeUpdater
                                    date={activity.created_at}
                                />
                            </Text>
                        </Flex>
                    ),
                },
            ]}
            onRowContextMenu={({ record, event }) =>
                showContextMenu([
                    {
                        key: 'delete',
                        icon: <IconTrash size={16} />,
                        title: 'Delete',
                        color: 'red',
                        onClick: () => {
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
                                            activityId: record.id,
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
                        },
                    },
                ])(event)
            }
        />
    )
}

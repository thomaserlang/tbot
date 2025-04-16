import { ErrorBox } from '@/components/error-box'
import { PageLoader } from '@/components/page-loader'
import { ChannelId } from '@/features/channel'
import { Provider } from '@/types/provider.type'
import { strDateFormat } from '@/utils/date'
import { pageRecordsFlatten } from '@/utils/page-records'
import { Button, Center, Flex } from '@mantine/core'
import humanizeDuration from 'humanize-duration'
import { DataTable } from 'mantine-datatable'
import { useGetChannelViewerStreams } from '../api/channel-viewer-streams'
import { ProviderViewerId } from '../types/viewer.type'

interface Props {
    channelId: ChannelId
    provider: Provider
    providerViewerId: ProviderViewerId
}

export function ViewerStreamsTable(props: Props) {
    const { data, isLoading, error, hasNextPage, fetchNextPage } =
        useGetChannelViewerStreams({
            ...props,
            params: {
                per_page: 3,
            },
        })

    if (isLoading) return <PageLoader />
    if (error) return <ErrorBox errorObj={error} />

    return (
        <Flex gap="0.5rem" direction="column" h="100%">
            <DataTable
                idAccessor={(row) => row.channel_provider_stream.id}
                records={pageRecordsFlatten(data)}
                fetching={isLoading}
                withTableBorder
                highlightOnHover
                columns={[
                    {
                        accessor: 'channel_provider_stream.started_at',
                        title: 'Date',
                        width: '1%',
                        noWrap: true,
                        render: (row) =>
                            strDateFormat(
                                row.channel_provider_stream.started_at
                            ),
                    },
                    {
                        accessor: 'viewer_watchtime.watchtime',
                        title: 'Watchtime',
                        render: (row) =>
                            humanizeDuration(
                                row.viewer_watchtime.watchtime * 1000
                            ),
                    },
                    {
                        accessor: 'channel_provider_stream.provider_stream_id',
                        title: 'Stream ID',
                        width: '1%',
                    },
                ]}
                flex={1}
            />
            {hasNextPage && (
                <Center>
                    <Button
                        color="gray"
                        variant="subtle"
                        size="compact-xs"
                        onClick={() => {
                            fetchNextPage()
                        }}
                    >
                        Load more
                    </Button>
                </Center>
            )}
        </Flex>
    )
}

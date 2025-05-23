import { pageRecordsFlatten } from '@/utils/page-records'
import { Box, Flex, Input } from '@mantine/core'
import { IconSearch } from '@tabler/icons-react'
import { DataTable } from 'mantine-datatable'
import { useGetChannels } from '../api/channels.api'
import { Channel } from '../types/channel.types'

interface Props {
    onSelect?: (channel: Channel) => void
}

export function SelectChannel({ onSelect }: Props) {
    const { data, fetchNextPage, isLoading, isFetchNextPageError } =
        useGetChannels()
    return (
        <Flex gap="1rem" direction="column">
            <Input
                placeholder="Search..."
                w="100%"
                rightSection={<IconSearch />}
            />

            <Box>
                <DataTable
                    records={pageRecordsFlatten(data)}
                    height={400}
                    fz="xl"
                    noHeader
                    withTableBorder
                    borderRadius="xs"
                    highlightOnHover
                    onScrollToBottom={fetchNextPage}
                    noRecordsText="No channels"
                    fetching={isLoading || isFetchNextPageError}
                    onRowClick={({ record }) => {
                        onSelect?.(record)
                    }}
                    columns={[
                        {
                            accessor: 'display_name',
                        },
                    ]}
                />
            </Box>
        </Flex>
    )
}

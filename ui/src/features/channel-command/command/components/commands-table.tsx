import { PageCursor } from '@/types/page-cursor.type'
import { pageRecordsFlatten } from '@/utils/page-records'
import { Anchor } from '@mantine/core'
import { IconBlocks } from '@tabler/icons-react'
import { InfiniteData, UseInfiniteQueryResult } from '@tanstack/react-query'
import { DataTable } from 'mantine-datatable'
import { Command } from '../types/command.types'
import { CommandMenu } from './command-menu'

interface Props {
    data: UseInfiniteQueryResult<InfiniteData<PageCursor<Command>>>
    onEditClick?: (command: Command) => void
}

export function CommandsTable({ data, onEditClick }: Props) {
    return (
        <DataTable
            records={pageRecordsFlatten(data.data)}
            withTableBorder
            highlightOnHover
            onScrollToBottom={() => data.fetchNextPage()}
            fetching={data.isFetching}
            h="100%"
            fz="md"
            noRecordsText="No commands, create one."
            noRecordsIcon={<IconBlocks size={80} />}
            columns={[
                {
                    accessor: 'cmds',
                    title: 'Command/Pattern',
                    width: '25%',

                    render: (row) => (
                        <Anchor onClick={() => onEditClick?.(row)}>
                            {row.cmds.map((cmd) => `!${cmd}`).join(', ')}
                            {!row.cmds && row.patterns?.join(', ')}
                        </Anchor>
                    ),
                },
                {
                    accessor: 'response',
                    title: 'Response',
                },
                {
                    accessor: '',
                    width: '1%',
                    render: (row) => (
                        <CommandMenu command={row} onEditClick={onEditClick} />
                    ),
                },
            ]}
        />
    )
}

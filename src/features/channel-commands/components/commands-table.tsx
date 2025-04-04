import { PageCursor } from '@/types/page-cursor.type'
import { pageRecordsFlatten } from '@/utils/page-records'
import { Anchor } from '@mantine/core'
import { InfiniteData, UseInfiniteQueryResult } from '@tanstack/react-query'
import { DataTable } from 'mantine-datatable'
import { Command } from '../commands.types'
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
            noRecordsText="No commands"
            columns={[
                {
                    accessor: 'cmds',
                    title: 'Command/Pattern',
                    width: '25%',

                    render: (row) => (
                        <Anchor size="sm" onClick={() => onEditClick?.(row)}>
                            {row.cmds.join(', ')} {row.patterns?.join(', ')}
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

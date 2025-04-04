import { PageCursor } from '@/types/page-cursor.type'
import { pageRecordsFlatten } from '@/utils/page-records'
import { Anchor } from '@mantine/core'
import { InfiniteData, UseInfiniteQueryResult } from '@tanstack/react-query'
import { DataTable } from 'mantine-datatable'
import { Timer, timerActiveModeLabels } from '../timer.types'
import { TimerMenu } from './timer-menu'

interface Props {
    data: UseInfiniteQueryResult<InfiniteData<PageCursor<Timer>>>
    onEditClick?: (command: Timer) => void
}

export function TimersTable({ data, onEditClick }: Props) {
    return (
        <DataTable
            records={pageRecordsFlatten(data.data)}
            withTableBorder
            highlightOnHover
            onScrollToBottom={() => data.fetchNextPage()}
            fetching={data.isFetching}
            h="100%"
            noRecordsText="No Timers"
            columns={[
                {
                    accessor: 'name',
                    title: 'Name',
                    width: '25%',
                    render: (row) => (
                        <Anchor size="sm" onClick={() => onEditClick?.(row)}>
                            {row.name}
                        </Anchor>
                    ),
                },
                {
                    accessor: 'interval',
                    title: 'Interval',
                    render: (row) => <span>{row.interval} minutes</span>,
                },
                {
                    accessor: 'active_mode',
                    title: 'Active when',
                    render: (row) => timerActiveModeLabels[row.active_mode],
                },
                {
                    accessor: 'enabled',
                    title: 'Enabled',
                    render: (row) => (row.enabled ? 'Yes' : 'No'),
                },
                {
                    accessor: '',
                    width: '1%',
                    render: (row) => (
                        <TimerMenu timer={row} onEditClick={onEditClick} />
                    ),
                },
            ]}
        />
    )
}

import { ErrorBox } from '@/components/error-box'
import { ChannelId } from '@/features/channel/types'
import { strDateFormat } from '@/utils/date'
import { pageRecordsFlatten } from '@/utils/page-records'
import { Anchor } from '@mantine/core'
import { DataTable } from 'mantine-datatable'
import { useGetQuotes } from '../api/quotes.api'
import { ChannelQuote } from '../types/quote.types'
import { QuoteContextMenu } from './quote-context-menu'

interface Props {
    channelId: ChannelId
    onEditClick?: (quote: ChannelQuote) => void
    onDeleted?: (quote: ChannelQuote) => void
}

export function QuotesTable({ channelId, onEditClick, onDeleted }: Props) {
    const { data, isLoading, error, fetchNextPage, isFetchingNextPage } =
        useGetQuotes({
            channelId,
        })
    if (error) return <ErrorBox errorObj={error} />

    return (
        <DataTable
            withTableBorder
            highlightOnHover
            noRecordsText="No quotes, create one!"
            height={'100%'}
            records={pageRecordsFlatten(data)}
            fz="md"
            onScrollToBottom={fetchNextPage}
            fetching={isLoading || isFetchingNextPage}
            columns={[
                {
                    accessor: 'number',
                    title: 'Number',
                    width: '1%',
                    textAlign: 'right',
                    render: (row) => (
                        <Anchor onClick={() => onEditClick?.(row)}>
                            {row.number}
                        </Anchor>
                    ),
                },
                { accessor: 'message', title: 'Quote' },
                {
                    accessor: 'created_by_display_name',
                    title: 'Created by',
                    width: '1%',
                    noWrap: true,
                },
                {
                    accessor: 'created_at',
                    title: 'Date',
                    width: '1%',
                    noWrap: true,
                    render: (row) => strDateFormat(row.created_at),
                },
                {
                    accessor: '',
                    title: '',
                    width: '1%',
                    noWrap: true,
                    render: (row) => (
                        <QuoteContextMenu
                            quote={row}
                            onEditClick={() => onEditClick?.(row)}
                            onDeleted={onDeleted}
                        />
                    ),
                },
            ]}
        />
    )
}

import { ErrorBox } from '@/components/error-box'
import { ChannelId } from '@/features/channel/types/channel.types'
import { pageRecordsFlatten } from '@/utils/page-records'
import { Anchor } from '@mantine/core'
import { DataTable } from 'mantine-datatable'
import { useState } from 'react'
import { ChatFilterId } from '../../../filter.types'
import { BannedTermMenu } from './banned-term-menu'
import { useGetBannedTerms } from './banned-terms.api'
import {
    BannedTerm,
    BannedTermId,
    bannedTermTypeLabels,
} from './banned-terms.types'
import { EditBannedTermModal } from './edit-banned-term-modal'

interface Props {
    channelId: ChannelId
    chatFilterId: ChatFilterId
    selectedId?: BannedTermId | null
    onUpdated?: (bannedTerm: BannedTerm) => void
}

export function BannedTermsTable({
    channelId,
    chatFilterId,
    selectedId,
    onUpdated,
}: Props) {
    const { data, isLoading, isFetchingNextPage, error, fetchNextPage } =
        useGetBannedTerms({
            channelId,
            chatFilterId,
        })
    const [editId, setEditId] = useState<BannedTermId | null>(null)

    if (error) return <ErrorBox errorObj={error} />

    return (
        <>
            <DataTable
                records={pageRecordsFlatten(data)}
                noHeader
                fetching={isLoading || isFetchingNextPage}
                noRecordsText="No banned terms"
                withTableBorder
                onScrollToBottom={fetchNextPage}
                highlightOnHover
                h="100%"
                rowBackgroundColor={(record) =>
                    record.id === selectedId
                        ? 'var(--tbot-selected-color)'
                        : undefined
                }
                columns={[
                    {
                        accessor: 'type',
                        width: '1%',
                        render: (row) => (
                            <Anchor size="sm" onClick={() => setEditId(row.id)}>
                                {bannedTermTypeLabels[row.type] || (
                                    <span>{row.type}</span>
                                )}
                            </Anchor>
                        ),
                    },
                    {
                        accessor: 'text',
                    },
                    {
                        accessor: '',
                        width: '1%',
                        render: (row) => (
                            <BannedTermMenu
                                bannedTerm={row}
                                channelId={channelId}
                                onEditClick={() => setEditId(row.id)}
                            />
                        ),
                    },
                ]}
            />
            {editId && (
                <EditBannedTermModal
                    channelId={channelId}
                    chatFilterId={chatFilterId}
                    bannedTermId={editId}
                    onClose={() => setEditId(null)}
                    onUpdated={(bannedTerm) => {
                        onUpdated?.(bannedTerm)
                    }}
                />
            )}
        </>
    )
}

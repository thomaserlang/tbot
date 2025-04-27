import { toastPromise } from '@/utils/toast'
import { ActionIcon, Menu, MenuItem } from '@mantine/core'
import { IconDotsVertical, IconEdit, IconTrash } from '@tabler/icons-react'
import { useDeleteQuote } from '../api/quote.api'
import { ChannelQuote } from '../types/quote.types'

interface Props {
    quote: ChannelQuote
    onEditClick?: (quote: ChannelQuote) => void
    onDeleted?: (quote: ChannelQuote) => void
}

export function QuoteContextMenu({ quote, onEditClick }: Props) {
    const deleteQuote = useDeleteQuote()

    return (
        <Menu width={200}>
            <Menu.Target>
                <ActionIcon variant="subtle" color="gray">
                    <IconDotsVertical size={16} />
                </ActionIcon>
            </Menu.Target>

            <Menu.Dropdown>
                <MenuItem
                    leftSection={<IconEdit size={14} />}
                    onClick={() => onEditClick?.(quote)}
                >
                    Edit
                </MenuItem>
                <Menu.Item
                    color="red"
                    leftSection={<IconTrash size={14} />}
                    onClick={() => {
                        toastPromise({
                            promise: deleteQuote.mutateAsync({
                                channelQuoteId: quote.id,
                                channelId: quote.channel_id,
                            }),
                            loading: {
                                title: 'Deleting quote',
                            },
                            success: {
                                title: 'Quote deleted',
                            },
                            error: {
                                title: 'Failed to delete quote',
                            },
                        })
                    }}
                >
                    Delete
                </Menu.Item>
            </Menu.Dropdown>
        </Menu>
    )
}

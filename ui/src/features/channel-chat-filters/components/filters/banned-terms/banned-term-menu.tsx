import { ChannelId } from '@/features/channel/types/channel.types'
import { toastPromise } from '@/utils/toast'
import { ActionIcon, Menu, MenuItem } from '@mantine/core'
import { IconDotsVertical, IconEdit, IconTrash } from '@tabler/icons-react'
import { useDeleteBannedTerm } from './banned-term.api'
import { BannedTerm } from './banned-terms.types'

interface Props {
    channelId: ChannelId
    bannedTerm: BannedTerm
    onEditClick?: (bannedTerm: BannedTerm) => void
    onDeleted?: (bannedTerm: BannedTerm) => void
}

export function BannedTermMenu({
    channelId,
    bannedTerm,
    onEditClick,
    onDeleted,
}: Props) {
    const deleteBannedTerm = useDeleteBannedTerm({
        onSuccess: () => {
            onDeleted?.(bannedTerm)
        },
    })

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
                    onClick={() => onEditClick?.(bannedTerm)}
                >
                    Edit
                </MenuItem>
                <Menu.Item
                    color="red"
                    leftSection={<IconTrash size={14} />}
                    onClick={() => {
                        toastPromise({
                            promise: deleteBannedTerm.mutateAsync({
                                bannedTermId: bannedTerm.id,
                                chatFilterId: bannedTerm.chat_filter_id,
                                channelId: channelId,
                            }),
                            loading: {
                                title: 'Deleting Timer',
                            },
                            success: {
                                title: 'Timer deleted',
                            },
                            error: {
                                title: 'Failed to delete Timer',
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

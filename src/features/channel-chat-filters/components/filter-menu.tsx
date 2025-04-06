import { toastPromise } from '@/utils/toast'
import { ActionIcon, Menu } from '@mantine/core'
import { IconDotsVertical, IconEdit, IconTrash } from '@tabler/icons-react'
import { useNavigate } from 'react-router-dom'
import { useDeleteChatFilter } from '../filter.api'
import { ChatFilterBase } from '../filter.types'

interface Props {
    filter: ChatFilterBase
    onDeleted?: (filter: ChatFilterBase) => void
    onEditClick?: (filter: ChatFilterBase) => void
}

export function FilterMenu({ filter }: Props) {
    const navigate = useNavigate()
    const deleteFilter = useDeleteChatFilter()

    return (
        <Menu width={200}>
            <Menu.Target>
                <ActionIcon variant="subtle" color="gray" size="sm">
                    <IconDotsVertical size={16} />
                </ActionIcon>
            </Menu.Target>
            <Menu.Dropdown>
                <Menu.Item
                    leftSection={<IconEdit size={16} />}
                    onClick={() => {
                        navigate(
                            `/channels/${filter.channel_id}/chat-filters/${filter.id}`
                        )
                    }}
                >
                    Edit
                </Menu.Item>
                <Menu.Item
                    leftSection={<IconTrash size={16} />}
                    color="red"
                    onClick={() => {
                        toastPromise({
                            promise: deleteFilter.mutateAsync({
                                channelId: filter.channel_id,
                                filterId: filter.id,
                            }),
                            success: {
                                title: 'Filter deleted',
                            },
                            error: {
                                title: 'Error deleting filter',
                            },
                            loading: {
                                title: 'Deleting filter...',
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

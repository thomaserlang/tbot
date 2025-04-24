import { toastPromise } from '@/utils/toast'
import { ActionIcon, Menu, MenuItem } from '@mantine/core'
import { IconDotsVertical, IconEdit, IconTrash } from '@tabler/icons-react'
import { useDeleteCommand } from '../command.api'
import { Command } from '../command.types'

interface Props {
    command: Command
    onEditClick?: (command: Command) => void
    onDeleted?: (command: Command) => void
}

export function CommandMenu({ command, onEditClick }: Props) {
    const deleteCmd = useDeleteCommand()

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
                    onClick={() => onEditClick?.(command)}
                >
                    Edit
                </MenuItem>
                <Menu.Item
                    color="red"
                    leftSection={<IconTrash size={14} />}
                    onClick={() => {
                        toastPromise({
                            promise: deleteCmd.mutateAsync({
                                commandId: command.id,
                                channelId: command.channel_id,
                            }),
                            loading: {
                                title: 'Deleting command',
                            },
                            success: {
                                title: 'Command deleted',
                            },
                            error: {
                                title: 'Failed to delete command',
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

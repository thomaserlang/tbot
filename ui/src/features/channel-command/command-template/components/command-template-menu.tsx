import { toastPromise } from '@/utils/toast'
import { ActionIcon, Menu, MenuItem } from '@mantine/core'
import { openConfirmModal } from '@mantine/modals'
import { IconDotsVertical, IconEdit, IconTrash } from '@tabler/icons-react'
import { deleteCommandTemplate } from '../api/command-template.api'
import { CommandTemplate } from '../types/command-template.types'

interface Props {
    commandTemplate: CommandTemplate
    onEditClick?: (command: CommandTemplate) => void
    onDeleted?: (command: CommandTemplate) => void
}

export function CommandTemplateMenu({ commandTemplate, onEditClick }: Props) {
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
                    onClick={() => onEditClick?.(commandTemplate)}
                >
                    Edit
                </MenuItem>
                <Menu.Item
                    color="red"
                    leftSection={<IconTrash size={14} />}
                    onClick={() => confirmDelete(commandTemplate)}
                >
                    Delete
                </Menu.Item>
            </Menu.Dropdown>
        </Menu>
    )
}

function confirmDelete(commandTemplate: CommandTemplate) {
    openConfirmModal({
        title: 'Delete command template',
        children: (
            <p>
                Are you sure you want to delete the command template{' '}
                <strong>{commandTemplate.title}</strong>? This action cannot be
                undone.
            </p>
        ),
        labels: { confirm: 'Delete Command Template', cancel: 'Cancel' },
        confirmProps: { color: 'red' },
        onConfirm: () => {
            toastPromise({
                promise: deleteCommandTemplate({
                    commandTemplateId: commandTemplate.id,
                }),
                loading: {
                    title: 'Deleting command template',
                },
                success: {
                    title: 'Command template deleted',
                },
                error: {
                    title: 'Failed to delete command template',
                },
            })
        },
    })
}

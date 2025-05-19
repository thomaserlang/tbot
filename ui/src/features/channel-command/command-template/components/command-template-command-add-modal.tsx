import { Modal } from '@mantine/core'
import { CommandCreate, CommandUpdate } from '../../command/types/command.types'
import { CommandTemplateCommandForm } from './command-template-command-add-form'

interface Props {
    opened: boolean
    initialValues?: CommandCreate | CommandUpdate
    onClose: () => void
    onSave: (command: CommandCreate | CommandUpdate) => void
}

export function CommandTemplateCommandAddModal({
    opened,
    initialValues,
    onClose,
    onSave,
}: Props) {
    return (
        <Modal opened={opened} onClose={onClose} title="Command" size="lg">
            {opened && (
                <CommandTemplateCommandForm
                    initialValues={initialValues}
                    onSave={onSave}
                />
            )}
        </Modal>
    )
}

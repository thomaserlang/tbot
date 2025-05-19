import { Modal } from '@mantine/core'
import { CommandTemplate } from '../types/command-template.types'
import { CommandTemplateCreateForm } from './command-template-create-form'

interface Props {
    opened: boolean
    onClose: () => void
    onCreated?: (template: CommandTemplate) => void
}

export function CommandTemplateCreateModal({
    opened,
    onClose,
    onCreated,
}: Props) {
    return (
        <Modal
            opened={opened}
            onClose={onClose}
            title="Create command template"
            size="lg"
        >
            {opened && (
                <CommandTemplateCreateForm
                    onCreated={(template) => {
                        onCreated?.(template)
                        onClose()
                    }}
                />
            )}
        </Modal>
    )
}

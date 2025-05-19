import { Box, Modal } from '@mantine/core'
import { CommandTemplate } from '../types/command-template.types'
import { CommandTemplateSelectTable } from './command-template-select-table'

interface Props {
    opened: boolean
    onClose: () => void
    onSelect: (commandTemplate: CommandTemplate) => void
}

export function CommandTemplateSelectModal({
    opened,
    onClose,
    onSelect,
}: Props) {
    return (
        <Modal opened={opened} onClose={onClose} title="Command Templates">
            {opened && (
                <Box h={350}>
                    <CommandTemplateSelectTable
                        onSelect={(commandTemplate) => {
                            onSelect?.(commandTemplate)
                            onClose()
                        }}
                    />
                </Box>
            )}
        </Modal>
    )
}

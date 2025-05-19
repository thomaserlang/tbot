import { Box, Button, Flex, Modal } from '@mantine/core'
import { useState } from 'react'
import { CommandCreate } from '../../command/types/command.types'
import { CommandTemplate } from '../types/command-template.types'
import { CommandTemplateCommandsTable } from './command-template-commands-table'

interface Props {
    opened: boolean
    commandTemplate: CommandTemplate
    onClose: () => void
    onSelect?: (commands: CommandCreate[]) => void
}

export function CommandTemplateCommandsSelectModal({
    commandTemplate,
    opened,
    onClose,
    onSelect,
}: Props) {
    const [selected, setSelected] = useState<CommandCreate[]>(
        commandTemplate.commands
    )

    return (
        <Modal
            opened={opened}
            onClose={onClose}
            title="Select commands to import"
            size="lg"
        >
            <Flex gap="1rem" direction="column">
                <Box h={300}>
                    <CommandTemplateCommandsTable
                        commands={commandTemplate.commands}
                        selectedCommands={selected}
                        onSelect={setSelected}
                    />
                </Box>

                <Flex justify="flex-end">
                    <Button
                        disabled={selected.length === 0}
                        onClick={() => {
                            onSelect?.(selected)
                            onClose()
                        }}
                    >
                        Import commands
                    </Button>
                </Flex>
            </Flex>
        </Modal>
    )
}

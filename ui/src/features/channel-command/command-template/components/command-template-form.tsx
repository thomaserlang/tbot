import { Box, Button, Flex, TextInput } from '@mantine/core'
import { UseFormReturnType } from '@mantine/form'
import { IconPlus } from '@tabler/icons-react'
import { useState } from 'react'
import {
    CommandTemplateCreate,
    CommandTemplateUpdate,
} from '../types/command-template.types'
import { CommandTemplateCommandAddModal } from './command-template-command-add-modal'
import { CommandTemplateCommandsTable } from './command-template-commands-table'

interface Props {
    form:
        | UseFormReturnType<CommandTemplateCreate>
        | UseFormReturnType<CommandTemplateUpdate>
}

export function CommandTemplateForm({ form }: Props) {
    const [addCommandOpened, setAddCommandOpened] = useState(false)
    const [editCommandIndex, setEditCommandIndex] = useState<number | null>(
        null
    )

    return (
        <>
            {addCommandOpened && (
                <CommandTemplateCommandAddModal
                    opened={addCommandOpened}
                    onClose={() => setAddCommandOpened(false)}
                    onSave={(command) => {
                        form.insertListItem('commands', command)
                        setAddCommandOpened(false)
                    }}
                />
            )}

            {editCommandIndex !== null && (
                <CommandTemplateCommandAddModal
                    opened={true}
                    onClose={() => setEditCommandIndex(null)}
                    onSave={(command) => {
                        form.replaceListItem(
                            'commands',
                            editCommandIndex,
                            command
                        )
                        setEditCommandIndex(null)
                    }}
                    initialValues={
                        form.getValues().commands?.[editCommandIndex]
                    }
                />
            )}

            <Flex gap="1rem" direction="column">
                <TextInput
                    label="Name"
                    key={form.key('title')}
                    {...form.getInputProps('title')}
                />

                <Flex gap="0.5rem" direction="column">
                    <Box>
                        <Button
                            size="compact-md"
                            fz="sm"
                            variant="light"
                            leftSection={<IconPlus size={16} />}
                            onClick={() => setAddCommandOpened(true)}
                        >
                            Add command
                        </Button>
                    </Box>

                    <CommandTemplateCommandsTable
                        commands={form.getValues().commands || []}
                        onDelete={(index) => {
                            form.removeListItem('commands', index)
                        }}
                        onEdit={(index) => {
                            setEditCommandIndex(index)
                        }}
                    />
                </Flex>
            </Flex>
        </>
    )
}

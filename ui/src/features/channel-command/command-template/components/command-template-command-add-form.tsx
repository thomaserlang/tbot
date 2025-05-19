import { Button, Flex } from '@mantine/core'
import { useForm } from '@mantine/form'
import { CommandForm } from '../../command/components/command-form'
import { COMMAND_INITIAL_VALUES } from '../../command/constants'
import { CommandCreate, CommandUpdate } from '../../command/types/command.types'

interface Props {
    initialValues?: CommandCreate | CommandUpdate
    onSave: (command: CommandCreate | CommandUpdate) => void
}

export function CommandTemplateCommandForm({ initialValues, onSave }: Props) {
    const form = useForm<CommandCreate | CommandUpdate>({
        mode: 'uncontrolled',
        initialValues: {
            ...COMMAND_INITIAL_VALUES,
            ...initialValues,
        },
        onSubmitPreventDefault: 'always',
    })
    return (
        <>
            <CommandForm form={form} />

            <Flex justify="flex-end" mt="0.5rem">
                <Button
                    type="submit"
                    onClick={() => {
                        form.onSubmit((values) => {
                            onSave(values)
                        })()
                    }}
                >
                    Save
                </Button>
            </Flex>
        </>
    )
}

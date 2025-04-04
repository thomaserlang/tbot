import { Alert, Button, Flex } from '@mantine/core'
import { useForm } from '@mantine/form'
import { AxiosError } from 'axios'
import { useUpdateCommand } from '../command.api'
import { Command, CommandCreate } from '../commands.types'
import { CommandForm } from './command-form'

interface Props {
    command: Command
    onUpdated?: (command: Command) => void
}

export function EditCommandForm({ command, onUpdated }: Props) {
    const update = useUpdateCommand({
        onSuccess: (data) => {
            onUpdated?.(data)
        },
        onError: (error) => {
            if (error instanceof AxiosError) {
                if (error.status === 422) {
                    for (const e of error.response?.data.detail) {
                        form.setFieldError(
                            e.loc[1],
                            e.msg.replace('String', '')
                        )
                    }
                }
            }
        },
    })
    const form = useForm<CommandCreate>({
        mode: 'uncontrolled',
        initialValues: command,
    })

    return (
        <form
            onSubmit={form.onSubmit((values) => {
                update.mutate({
                    channelId: command.channel_id,
                    commandId: command.id,
                    data: values,
                })
            })}
        >
            <Flex gap="1rem" direction="column">
                <CommandForm form={form} />

                {update.isError && (
                    <Alert color="red" title="Failed to update the command" />
                )}

                <Flex>
                    <Button ml="auto" type="submit" loading={update.isPending}>
                        Update
                    </Button>
                </Flex>
            </Flex>
        </form>
    )
}

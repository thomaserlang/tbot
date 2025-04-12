import { Alert, Button, Flex } from '@mantine/core'
import { useForm } from '@mantine/form'
import { AxiosError } from 'axios'
import { useUpdateCommand } from '../command.api'
import { Command, CommandUpdate } from '../command.types'
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
    const form = useForm<CommandUpdate>({
        mode: 'uncontrolled',
        initialValues: {
            cmds: command.cmds,
            patterns: command.patterns,
            response: command.response,
            active_mode: command.active_mode,
            global_cooldown: command.global_cooldown,
            chatter_cooldown: command.chatter_cooldown,
            mod_cooldown: command.mod_cooldown,
            enabled: command.enabled,
            public: command.public,
            access_level: command.access_level,
            provider: command.provider,
            group_name: command.group_name,
        },
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
                        Save
                    </Button>
                </Flex>
            </Flex>
        </form>
    )
}

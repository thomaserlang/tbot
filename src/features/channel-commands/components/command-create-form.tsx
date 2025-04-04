import { ChannelId } from '@/features/channel/types'
import { AccessLevel } from '@/types/access-level.type'
import { Alert, Button, Flex } from '@mantine/core'
import { useForm } from '@mantine/form'
import { AxiosError } from 'axios'
import { useCreateCommand } from '../command.api'
import { Command, CommandCreate } from '../commands.types'
import { CommandForm } from './command-form'

interface Props {
    channelId: ChannelId
    onCreated: (command: Command) => void
}

export function CreateCommandForm({ channelId, onCreated }: Props) {
    const create = useCreateCommand({
        onSuccess: (data) => {
            onCreated(data)
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
        initialValues: {
            cmds: [],
            patterns: [],
            response: '',
            active_mode: 'always',
            global_cooldown: 5,
            chatter_cooldown: 15,
            mod_cooldown: 0,
            enabled: true,
            public: true,
            access_level: AccessLevel.PUBLIC,
            provider: 'all',
        },
    })

    return (
        <form
            onSubmit={form.onSubmit((values) => {
                create.mutate({
                    channelId,
                    data: values,
                })
            })}
        >
            <Flex gap="1rem" direction="column">
                <CommandForm form={form} />

                {create.isError && (
                    <Alert color="red" title="Failed to create the command" />
                )}

                <Flex>
                    <Button ml="auto" type="submit" loading={create.isPending}>
                        Create
                    </Button>
                </Flex>
            </Flex>
        </form>
    )
}

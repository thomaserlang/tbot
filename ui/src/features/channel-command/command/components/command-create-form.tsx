import { ChannelId } from '@/features/channel/types/channel.types'
import { setFormErrors } from '@/utils/form'
import { toastSuccess } from '@/utils/toast'
import { Alert, Button, Flex } from '@mantine/core'
import { useForm } from '@mantine/form'
import { useCreateCommand } from '../api/command.api'
import { COMMAND_INITIAL_VALUES } from '../constants'
import { Command, CommandCreate } from '../types/command.types'
import { CommandForm } from './command-form'

interface Props {
    channelId: ChannelId
    initialValues?: CommandCreate
    onCreated: (command: Command) => void
}

export function CommandCreateForm({
    initialValues,
    channelId,
    onCreated,
}: Props) {
    const create = useCreateCommand({
        onSuccess: (data) => {
            toastSuccess('Command created')
            onCreated(data)
        },
        onError: (error) => {
            if (error.status === 422) setFormErrors(form, error.response.data)
        },
    })
    const form = useForm<CommandCreate>({
        mode: 'controlled',
        initialValues: {
            ...COMMAND_INITIAL_VALUES,
            ...initialValues,
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
                        Save
                    </Button>
                </Flex>
            </Flex>
        </form>
    )
}

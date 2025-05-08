import { ChannelId } from '@/features/channel/types'
import { setFormErrors } from '@/utils/form'
import { toastError, toastSuccess } from '@/utils/toast'
import { Button, Flex, TextInput } from '@mantine/core'
import { useForm } from '@mantine/form'
import { useCreateQueue } from '../api/queue.api'
import { Queue } from '../types/queue.types'

interface Props {
    channelId: ChannelId
    onCreated?: (queue: Queue) => void
}

export function QueueCreateForm({ channelId, onCreated }: Props) {
    const form = useForm({
        initialValues: {
            name: '',
        },
    })
    const create = useCreateQueue({
        onSuccess: (data) => {
            onCreated?.(data)
            toastSuccess('Queue created')
        },
        onError: (error) => {
            if (error.status === 422) setFormErrors(form, error.response.data)
            else toastError(error)
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
                <TextInput
                    label="Queue Name"
                    data-autofocus
                    {...form.getInputProps('name')}
                />

                <Flex>
                    <Button loading={create.isPending} ml="auto" type="submit">
                        Save
                    </Button>
                </Flex>
            </Flex>
        </form>
    )
}

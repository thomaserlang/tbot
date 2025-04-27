import { ChannelId } from '@/features/channel/types'
import { setFormErrors } from '@/utils/form'
import { Alert, Button, Flex } from '@mantine/core'
import { useForm } from '@mantine/form'
import { useCreateTimer } from '../timer.api'
import { Timer, TimerCreate } from '../timer.types'
import { TimerForm } from './timer-form'

interface Props {
    channelId: ChannelId
    onCreated: (timer: Timer) => void
}

export function CreateTimerForm({ channelId, onCreated }: Props) {
    const create = useCreateTimer({
        onSuccess: (data) => {
            onCreated(data)
        },
        onError: (error) => {
            if (error.status === 422) setFormErrors(form, error.response.data)
        },
    })
    const form = useForm<TimerCreate>({
        mode: 'uncontrolled',
        initialValues: {
            name: '',
            messages: [''],
            interval: 30,
            enabled: true,
            provider: 'all',
            pick_mode: 'order',
            active_mode: 'online',
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
                <TimerForm form={form} />

                {create.isError && (
                    <Alert color="red" title="Failed to create the timer" />
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

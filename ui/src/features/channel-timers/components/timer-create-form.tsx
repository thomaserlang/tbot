import { ChannelId } from '@/features/channel/types'
import { Alert, Button, Flex } from '@mantine/core'
import { useForm } from '@mantine/form'
import { AxiosError } from 'axios'
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
            if (error instanceof AxiosError) {
                if (error.status === 422) {
                    for (const e of error.response?.data.detail) {
                        form.setFieldError(
                            e.loc.slice(1).join('.'),
                            e.msg.replace('String', '')
                        )
                    }
                }
            }
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

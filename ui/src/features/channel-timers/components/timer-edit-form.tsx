import { set_form_errors } from '@/utils/form'
import { Alert, Button, Flex } from '@mantine/core'
import { useForm } from '@mantine/form'
import { useUpdateTimer } from '../timer.api'
import { Timer, TimerUpdate } from '../timer.types'
import { TimerForm } from './timer-form'

interface Props {
    timer: Timer
    onUpdated?: (timer: Timer) => void
}

export function EditTimerForm({ timer, onUpdated }: Props) {
    const update = useUpdateTimer({
        onSuccess: (data) => {
            onUpdated?.(data)
        },
        onError: (error) => {
            if (error.status === 422) set_form_errors(form, error.response.data)
        },
    })
    const form = useForm<TimerUpdate>({
        mode: 'uncontrolled',
        initialValues: {
            name: timer.name,
            interval: timer.interval,
            active_mode: timer.active_mode,
            pick_mode: timer.pick_mode,
            enabled: timer.enabled,
            messages: timer.messages,
            provider: timer.provider,
        },
    })

    return (
        <form
            onSubmit={form.onSubmit((values) => {
                update.mutate({
                    channelId: timer.channel_id,
                    timerId: timer.id,
                    data: values,
                })
            })}
        >
            <Flex gap="1rem" direction="column">
                <TimerForm form={form} />

                {update.isError && (
                    <Alert color="red" title="Failed to update the timer" />
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

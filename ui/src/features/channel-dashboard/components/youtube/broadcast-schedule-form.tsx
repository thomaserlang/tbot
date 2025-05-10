import { TextareaLimitIndicator } from '@/components/textarea-limit-indicator'
import { Button, Flex, Select } from '@mantine/core'
import { DateTimePicker } from '@mantine/dates'
import { useForm } from '@mantine/form'
import dayjs from 'dayjs'
import { LiveBroadcastInsert } from './youtube.types'

interface Props {
    initialValues: LiveBroadcastInsert
    isPending?: boolean
    onSave: (values: LiveBroadcastInsert) => void
}

export function BroadcastScheduleForm({
    initialValues,
    isPending,
    onSave,
}: Props) {
    const form = useForm({
        initialValues: initialValues,
    })

    return (
        <form
            onSubmit={form.onSubmit((values) => {
                values.snippet.scheduledStartTime = dayjs(
                    values.snippet.scheduledStartTime
                ).format('YYYY-MM-DDTHH:mm:ssZ')
                onSave(values)
            })}
        >
            <Flex direction="column" gap="1rem">
                <Flex gap="1rem">
                    <DateTimePicker
                        label="Start time"
                        placeholder="Start time"
                        clearable={false}
                        highlightToday
                        weekendDays={[]}
                        minDate={dayjs().format('YYYY-MM-DD')}
                        key={form.key('snippet.scheduledStartTime')}
                        {...form.getInputProps('snippet.scheduledStartTime')}
                    />

                    <Select
                        label="Privacy"
                        data={[
                            { value: 'private', label: 'Private' },
                            { value: 'unlisted', label: 'Unlisted' },
                            { value: 'public', label: 'Public' },
                        ]}
                        key={form.key('status.privacyStatus')}
                        {...form.getInputProps('status.privacyStatus')}
                    />
                </Flex>

                <TextareaLimitIndicator
                    label="Title"
                    placeholder="Title"
                    maxLength={100}
                    key={form.key('snippet.title')}
                    {...form.getInputProps('snippet.title')}
                />

                <Flex>
                    <Button loading={isPending} ml="auto" type="submit">
                        Create Scheduled Broadcast
                    </Button>
                </Flex>
            </Flex>
        </form>
    )
}

import { ChannelProvider } from '@/features/channel-providers'
import { toastError, toastSuccess } from '@/utils/toast'
import { Button, Modal } from '@mantine/core'
import { useDisclosure } from '@mantine/hooks'
import { IconCalendar } from '@tabler/icons-react'
import dayjs from 'dayjs'
import { BroadcastScheduleForm } from './broadcast-schedule-form'
import { useCreateBroadcast } from './youtube.api'

interface Props {
    channelProvider: ChannelProvider
}

export function BroadcastScheduleButton({ channelProvider }: Props) {
    const [opened, { close, open }] = useDisclosure(false)
    const create = useCreateBroadcast({
        onSuccess: () => {
            toastSuccess('Broadcast created')
            close()
        },
        onError: (error) => {
            toastError(error)
        },
    })

    if (channelProvider.stream_id) return

    return (
        <>
            <Button
                variant="light"
                loading={create.isPending}
                onClick={open}
                leftSection={<IconCalendar size={16} />}
                size="xs"
            >
                Schedule Broadcast
            </Button>

            <Modal title="Schedule Broadcast" opened={opened} onClose={close}>
                <BroadcastScheduleForm
                    isPending={create.isPending}
                    initialValues={{
                        snippet: {
                            scheduledStartTime: dayjs()
                                .hour(dayjs().hour() + 1)
                                .minute(0)
                                .second(0)
                                .millisecond(0)
                                .toDate(),
                            title: channelProvider.stream_title || '',
                        },
                        status: {
                            privacyStatus: 'public',
                        },
                    }}
                    onSave={(values) => {
                        create.mutateAsync({
                            channelId: channelProvider.channel_id,
                            channelProviderId: channelProvider.id,
                            data: values,
                        })
                    }}
                />
            </Modal>
        </>
    )
}

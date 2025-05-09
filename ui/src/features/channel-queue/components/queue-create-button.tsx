import { ChannelId } from '@/features/channel/types/channel.types'
import { Button, Modal } from '@mantine/core'
import { useDisclosure } from '@mantine/hooks'
import { useNavigate } from 'react-router-dom'
import { QueueCreateForm } from './queue-create-form'

interface Props {
    channelId: ChannelId
}

export function QueueCreateButton({ channelId }: Props) {
    const [opened, { open, close }] = useDisclosure(false)
    const navigate = useNavigate()

    return (
        <>
            <Button onClick={open} variant="light">
                Create Queue
            </Button>

            <Modal
                title="Create Queue"
                size="xs"
                opened={opened}
                onClose={close}
            >
                {opened && (
                    <QueueCreateForm
                        channelId={channelId}
                        onCreated={(queue) => {
                            navigate(
                                `/channels/${channelId}/queues/${queue.id}`
                            )
                            close()
                        }}
                    />
                )}
            </Modal>
        </>
    )
}

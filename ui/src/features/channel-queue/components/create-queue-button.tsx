import { ChannelId } from '@/features/channel/types'
import { Button, Modal } from '@mantine/core'
import { useDisclosure } from '@mantine/hooks'
import { CreateQueueForm } from './create-queue-form'

interface Props {
    channelId: ChannelId
}

export function CreateQueueButton({ channelId }: Props) {
    const [opened, { open, close }] = useDisclosure(false)

    return (
        <>
            <Button size="lg" onClick={open} variant="light">
                Create Queue
            </Button>

            <Modal
                title="Create Queue"
                size="xs"
                opened={opened}
                onClose={close}
            >
                {opened && (
                    <CreateQueueForm
                        channelId={channelId}
                        onCreated={() => {
                            close()
                        }}
                    />
                )}
            </Modal>
        </>
    )
}

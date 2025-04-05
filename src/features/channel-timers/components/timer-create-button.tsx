import { ChannelId } from '@/features/channel'
import { Button, Modal } from '@mantine/core'
import { useDisclosure } from '@mantine/hooks'
import { IconPlus } from '@tabler/icons-react'
import { Timer } from '../timer.types'
import { CreateTimerForm } from './timer-create-form'

interface Props {
    channelId: ChannelId
    onCreated?: (timer: Timer) => void
}

export function CreatetimerButton({ channelId, onCreated }: Props) {
    const [opened, { open, close }] = useDisclosure(false)
    return (
        <>
            <Button
                ml="auto"
                variant="light"
                leftSection={<IconPlus size={14} />}
                onClick={open}
            >
                Create Timer
            </Button>

            <Modal
                size="lg"
                opened={opened}
                onClose={close}
                title="Create Timer"
            >
                <CreateTimerForm
                    channelId={channelId}
                    onCreated={(timer) => {
                        onCreated?.(timer)
                        close()
                    }}
                />
            </Modal>
        </>
    )
}

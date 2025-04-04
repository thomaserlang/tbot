import { ChannelId } from '@/features/channel/types'
import { Button, Modal } from '@mantine/core'
import { useDisclosure } from '@mantine/hooks'
import { IconPlus } from '@tabler/icons-react'
import { Command } from '../command.types'
import { CreateCommandForm } from './command-create-form'

interface Props {
    channelId: ChannelId
    onCreated?: (command: Command) => void
}

export function CreateCommandButton({ channelId, onCreated }: Props) {
    const [opened, { open, close }] = useDisclosure(false)
    return (
        <>
            <Button
                ml="auto"
                variant="light"
                rightSection={<IconPlus size={14} />}
                onClick={open}
            >
                Create
            </Button>

            <Modal
                size="lg"
                opened={opened}
                onClose={close}
                title="Create Command"
            >
                <CreateCommandForm
                    channelId={channelId}
                    onCreated={(command) => {
                        onCreated?.(command)
                        close()
                    }}
                />
            </Modal>
        </>
    )
}

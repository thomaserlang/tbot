import { ChannelId } from '@/features/channel/types'
import { Button } from '@mantine/core'
import { useDisclosure } from '@mantine/hooks'
import { IconPlus } from '@tabler/icons-react'
import { Command } from '../types/command.types'
import { CommandCreateModal } from './command-create-modal'

interface Props {
    channelId: ChannelId
    onCreated?: (command: Command) => void
}

export function CommandCreateButton({ channelId, onCreated }: Props) {
    const [opened, { open, close }] = useDisclosure(false)
    return (
        <>
            <Button
                ml="auto"
                variant="light"
                leftSection={<IconPlus size={14} />}
                onClick={open}
            >
                Create Command
            </Button>

            <CommandCreateModal
                channelId={channelId}
                opened={opened}
                onClose={close}
                onCreated={onCreated}
            />
        </>
    )
}

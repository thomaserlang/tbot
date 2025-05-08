import { ChannelId } from '@/features/channel/types'
import { Modal } from '@mantine/core'
import { Command, CommandCreate } from '../types/command.types'
import { CommandCreateForm } from './command-create-form'

interface Props {
    channelId: ChannelId
    opened: boolean
    initialValues?: CommandCreate
    onClose: () => void
    onCreated?: (command: Command) => void
}

export function CommandCreateModal({
    channelId,
    opened,
    initialValues,
    onClose,
    onCreated,
}: Props) {
    return (
        <Modal
            size="lg"
            opened={opened}
            onClose={onClose}
            title="Create Command"
        >
            {opened && (
                <CommandCreateForm
                    channelId={channelId}
                    initialValues={initialValues}
                    onCreated={(command) => {
                        onCreated?.(command)
                        onClose()
                    }}
                />
            )}
        </Modal>
    )
}

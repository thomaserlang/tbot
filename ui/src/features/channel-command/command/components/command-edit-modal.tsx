import { ErrorBox } from '@/components/error-box'
import { PageLoader } from '@/components/page-loader'
import { ChannelId } from '@/features/channel'
import { Modal } from '@mantine/core'
import { useGetCommand } from '../api/command.api'
import { CommandId } from '../types/command.types'
import { CommandEditForm } from './command-edit-form'

interface Props {
    channelId: ChannelId
    commandId: CommandId
    onClose: () => void
}

export function CommandEditModal({ channelId, commandId, onClose }: Props) {
    const { isLoading, error, data } = useGetCommand({
        channelId,
        commandId,
    })
    return (
        <Modal
            size="lg"
            opened={!!commandId}
            onClose={onClose}
            title="Edit Command"
        >
            {isLoading && <PageLoader />}
            {error && <ErrorBox errorObj={error} />}
            {data && (
                <CommandEditForm
                    command={data}
                    onUpdated={() => {
                        onClose()
                    }}
                />
            )}
        </Modal>
    )
}

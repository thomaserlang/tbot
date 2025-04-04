import { ErrorBox } from '@/components/error-box'
import { PageLoader } from '@/components/page-loader'
import { ChannelId } from '@/features/channel'
import { Modal } from '@mantine/core'
import { useGetCommand } from '../command.api'
import { CommandId } from '../commands.types'
import { EditCommandForm } from './command-edit-form'

interface Props {
    channelId: ChannelId
    commandId: CommandId
    onClose: () => void
}

export function EditCommandModal({ channelId, commandId, onClose }: Props) {
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
                <EditCommandForm
                    command={data}
                    onUpdated={() => {
                        onClose()
                    }}
                />
            )}
        </Modal>
    )
}

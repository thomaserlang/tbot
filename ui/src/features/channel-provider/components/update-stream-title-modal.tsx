import { providerInfo } from '@/constants'
import { Modal } from '@mantine/core'
import { ChannelProvider } from '../channel-provider.types'
import { UpdateStreamTitleForm } from './update-stream-title-form'

interface Props {
    channelProvider: ChannelProvider
    onClose: () => void
    opened: boolean
}

export function UpdateStreamTitleModal({
    channelProvider,
    onClose,
    opened,
}: Props) {
    return (
        <Modal
            opened={opened}
            onClose={onClose}
            title={`${
                providerInfo[channelProvider.provider].name ||
                channelProvider.provider
            } - Update Stream Title`}
        >
            {opened && (
                <UpdateStreamTitleForm
                    channelProvider={channelProvider}
                    onClose={onClose}
                />
            )}
        </Modal>
    )
}

import { ErrorBox } from '@/components/error-box'
import { PageLoader } from '@/components/page-loader'
import { ChannelId } from '@/features/channel/types'
import { providers } from '@/types/provider.type'
import { Modal } from '@mantine/core'
import { useGetChannelProvider } from '../channel-provider.api'
import { ChannelProviderId } from '../channel-provider.types'
import { ProviderView } from './channel-provider-view'

interface Props {
    channelId: ChannelId
    channelProviderId: ChannelProviderId
    onClose: () => void
}

export function ChannelProviderModal({
    channelId,
    channelProviderId: channelProviderId,
    onClose,
}: Props) {
    const { isLoading, error, data } = useGetChannelProvider({
        channelId,
        channelProviderId: channelProviderId,
    })
    return (
        <Modal
            size="lg"
            opened={!!channelProviderId}
            onClose={onClose}
            title={
                data
                    ? providers[data.provider].name || data.provider
                    : 'Provider settings'
            }
        >
            {isLoading && <PageLoader />}

            {error && <ErrorBox errorObj={error} />}

            {data && <ProviderView provider={data} onDeleted={onClose} />}
        </Modal>
    )
}

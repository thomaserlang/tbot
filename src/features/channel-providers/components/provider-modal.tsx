import { ErrorBox } from '@/components/error-box'
import { PageLoader } from '@/components/page-loader'
import { ChannelId } from '@/features/channel/types'
import { providerLabels } from '@/types/provider.type'
import { Modal } from '@mantine/core'
import { useGetProvider } from '../provider.api'
import { ChannelProviderId } from '../provider.types'
import { ProviderView } from './provider-view'

interface Props {
    channelId: ChannelId
    providerId: ChannelProviderId
    onClose: () => void
}

export function ProviderModal({ channelId, providerId, onClose }: Props) {
    const { isLoading, error, data } = useGetProvider({
        channelId,
        providerId,
    })
    return (
        <Modal
            size="lg"
            opened={!!providerId}
            onClose={onClose}
            title={
                data
                    ? providerLabels[data.provider] || data.provider
                    : 'Provider settings'
            }
        >
            {isLoading && <PageLoader />}
            {error && <ErrorBox errorObj={error} />}
            {data && <ProviderView provider={data} />}
        </Modal>
    )
}

import { ErrorBox } from '@/components/error-box'
import { PageLoader } from '@/components/page-loader'
import { providerInfo } from '@/constants'
import { Provider } from '@/types/provider.type'
import { Modal } from '@mantine/core'
import { useGetSystemProviderBot } from '../provider-bot.api'
import { ProviderBotView } from './provider-bot-view'

interface Props {
    provider: Provider
    onClose: () => void
}

export function ProviderBotModal({ provider, onClose }: Props) {
    const { isLoading, error, data } = useGetSystemProviderBot({
        provider,
    })
    return (
        <Modal
            size="lg"
            opened={!!provider}
            onClose={onClose}
            title={
                data
                    ? providerInfo[data.provider].name || data.provider
                    : 'Provider Bot'
            }
        >
            {isLoading && <PageLoader />}

            {error && <ErrorBox errorObj={error} />}

            {data && <ProviderBotView provider={data} onDeleted={onClose} />}
        </Modal>
    )
}

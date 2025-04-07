import { ErrorBox } from '@/components/error-box'
import { PageLoader } from '@/components/page-loader'
import { Container, Flex, Title } from '@mantine/core'
import { useNavigate, useParams } from 'react-router-dom'
import { useCurrentChannel } from '../channel/current-channel.provider'
import { ProviderModal } from './components/provider-modal'
import { ProvidersView } from './components/providers-view'
import { ChannelProviderId } from './provider.types'
import { useGetProviders } from './providers.api'

export function Component() {
    const channel = useCurrentChannel()
    const { providerId } = useParams<{ providerId?: ChannelProviderId }>()
    const { data, isLoading, error } = useGetProviders({
        channelId: channel.id,
    })
    const navigate = useNavigate()

    return (
        <Container>
            <Flex direction="column" gap="1rem">
                <Title order={2}>Providers</Title>

                {isLoading && <PageLoader />}

                {error && <ErrorBox errorObj={error} />}

                {data && <ProvidersView providers={data} />}
            </Flex>
            {providerId && (
                <ProviderModal
                    channelId={channel.id}
                    providerId={providerId}
                    onClose={() => {
                        navigate(`/channels/${channel.id}/providers`)
                    }}
                />
            )}
        </Container>
    )
}

import { ErrorBox } from '@/components/error-box'
import { PageLoader } from '@/components/page-loader'
import { useDocumentTitle } from '@/utils/document-title'
import { Container, Flex, Title } from '@mantine/core'
import { useNavigate, useParams } from 'react-router-dom'
import { useCurrentChannel } from '../channel/current-channel.provider'
import { useGetChannelProviders } from './api/channel-providers.api'
import { ChannelProviderId } from './channel-provider.types'
import { AddChannelProviderButton } from './components/add-channel-provider-button'
import { ChannelProviderModal } from './components/channel-provider-modal'
import { ProvidersView } from './components/channel-providers-view'
import { TiktokUsernameModal } from './components/tiktok-username-modal'

export function Component() {
    const channel = useCurrentChannel()
    const { channelProviderId, provider } = useParams<{
        channelProviderId?: ChannelProviderId
        provider?: string
    }>()
    const { data, isLoading, error } = useGetChannelProviders({
        channelId: channel.id,
    })
    const navigate = useNavigate()
    useDocumentTitle(`Channel Providers - ${channel.display_name}`)

    return (
        <Container>
            <Flex direction="column" gap="1rem">
                <Flex>
                    <Title order={2}>Providers</Title>
                    <AddChannelProviderButton channelId={channel.id} />
                </Flex>

                {isLoading && <PageLoader />}

                {error && <ErrorBox errorObj={error} />}

                {data && <ProvidersView channelProviders={data} />}
            </Flex>

            {channelProviderId && (
                <ChannelProviderModal
                    channelId={channel.id}
                    channelProviderId={channelProviderId}
                    onClose={() => {
                        navigate(`/channels/${channel.id}/providers`)
                    }}
                />
            )}

            {provider && (
                <TiktokUsernameModal
                    channelId={channel.id}
                    opened={!!provider}
                    onClose={() => {
                        navigate(`/channels/${channel.id}/providers`)
                    }}
                />
            )}
        </Container>
    )
}

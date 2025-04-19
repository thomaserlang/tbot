import { ErrorBox } from '@/components/error-box'
import { PageLoader } from '@/components/page-loader'
import { useDocumentTitle } from '@/utils/document-title'
import { Container, Flex, Title } from '@mantine/core'
import { useNavigate, useParams } from 'react-router-dom'
import { useCurrentChannel } from '../channel/current-channel.provider'
import { ChannelProviderId } from './channel-provider.types'
import { useGetProviders } from './channel-providers.api'
import { AddChannelProviderButton } from './components/add-channel-provider-button'
import { ChannelProviderModal } from './components/channel-provider-modal'
import { ProvidersView } from './components/channel-providers-view'

export function Component() {
    const channel = useCurrentChannel()
    const { providerId } = useParams<{ providerId?: ChannelProviderId }>()
    const { data, isLoading, error } = useGetProviders({
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

            {providerId && (
                <ChannelProviderModal
                    channelId={channel.id}
                    channelProviderId={providerId}
                    onClose={() => {
                        navigate(`/channels/${channel.id}/providers`)
                    }}
                />
            )}
        </Container>
    )
}

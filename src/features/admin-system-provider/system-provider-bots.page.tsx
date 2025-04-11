import { ErrorBox } from '@/components/error-box'
import { PageLoader } from '@/components/page-loader'
import { Provider } from '@/types/provider.type'
import { useDocumentTitle } from '@/utils/document-title'
import { Container, Flex, Title } from '@mantine/core'
import { useNavigate, useParams } from 'react-router-dom'
import { AddProviderButton } from './components/add-provider-bot-button'
import { ProviderBotModal } from './components/provider-bot-modal'
import { ProviderBotsView } from './components/providers-bot-view'
import { useGetSystemProviderBots } from './provider-bots.api'

export function Component() {
    const { provider } = useParams<{ provider?: Provider }>()
    const { data, isLoading, error } = useGetSystemProviderBots()
    const navigate = useNavigate()
    useDocumentTitle(`System Provider Bots`)

    return (
        <Container>
            <Flex direction="column" gap="1rem">
                <Flex>
                    <Title order={2}>System Provider Bots</Title>
                    <AddProviderButton />
                </Flex>

                {isLoading && <PageLoader />}

                {error && <ErrorBox errorObj={error} />}

                {data && <ProviderBotsView providerBots={data} />}
            </Flex>

            {provider && (
                <ProviderBotModal
                    provider={provider}
                    onClose={() => {
                        navigate(`/admin/system-provider-bots`)
                    }}
                />
            )}
        </Container>
    )
}

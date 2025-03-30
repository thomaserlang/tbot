import { ErrorBox } from '@/components/error-box'
import { PageLoader } from '@/components/page-loader'
import { Flex, Paper, Text, Title } from '@mantine/core'
import { useCurrentChannel } from '../channel/current-channel.provider'
import { useGetChannelProviders } from './channel-providers.api'

export function Component() {
    const channel = useCurrentChannel()
    const { data, isLoading, error } = useGetChannelProviders({
        channelId: channel.id,
    })

    return (
        <Flex direction="column" gap="1rem">
            <Title order={2}>Providers</Title>

            {isLoading && <PageLoader />}

            {error && <ErrorBox errorObj={error} />}

            {data && (
                <Flex gap="2rem" wrap={'wrap'}>
                    {data?.map((provider) => (
                        <Paper key={provider.id} withBorder p="0.5rem" w={300}>
                            <Title tt="capitalize" order={3}>
                                {provider.provider}
                            </Title>
                            <Text c="dimmed">{provider.name}</Text>
                        </Paper>
                    ))}
                </Flex>
            )}
        </Flex>
    )
}

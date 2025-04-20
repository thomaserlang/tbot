import { ErrorBox } from '@/components/error-box'
import { PageLoader } from '@/components/page-loader'
import { ChannelId } from '@/features/channel'
import { useGetChannelProviders } from '@/features/channel-providers'
import { providers } from '@/types/provider.type'
import { Flex } from '@mantine/core'
import { DashboardChannelProvider } from './dashboard-channel-provider'

interface Props {
    channelId: ChannelId
}

export function DashboardProviders({ channelId }: Props) {
    const channelProviders = useGetChannelProviders({
        channelId,
        options: {
            refetchInterval: 5000,
        },
    })

    if (channelProviders.isLoading) return <PageLoader />
    if (channelProviders.error)
        return <ErrorBox errorObj={channelProviders.error} />

    return (
        <Flex direction="row" gap="1rem" wrap={'wrap'}>
            {channelProviders.data
                ?.filter((f) => providers[f.provider])
                .map((channelProvider) => (
                    <DashboardChannelProvider
                        key={channelProvider.id}
                        channelProvider={channelProvider}
                    />
                ))}
        </Flex>
    )
}

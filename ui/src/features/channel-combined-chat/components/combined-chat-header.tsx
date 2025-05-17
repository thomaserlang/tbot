import { TimeCounter } from '@/components/time-counter'
import { ViewerCount } from '@/components/viewer-count'
import { providerInfo } from '@/constants'
import { useCurrentChannel } from '@/features/channel'
import { useGetChannelProviders } from '@/features/channel-provider'
import { Divider, Flex, Text } from '@mantine/core'
import { Fragment } from 'react/jsx-runtime'

export function CombinedChatHeader() {
    return (
        <Flex justify="space-between">
            <Text fw={500}>Chat</Text> <ChannelProvidersLiveStatus />
        </Flex>
    )
}

export function ChannelProvidersLiveStatus() {
    const channel = useCurrentChannel()
    const { data } = useGetChannelProviders({
        channelId: channel.id,
        options: {
            refetchInterval: 5000,
        },
    })

    return (
        <Flex gap="1rem" align="center">
            {data
                ?.filter((f) => f.stream_live)
                .map((channelProvider) => (
                    <Fragment key={channelProvider.id}>
                        <Divider orientation="vertical" />

                        <Flex gap="0.35rem" align="center">
                            {providerInfo[channelProvider.provider].icon}
                            <ViewerCount
                                count={channelProvider.stream_viewer_count}
                            />
                            {channelProvider.stream_live_at && (
                                <Text size="sm" c="dimmed">
                                    <TimeCounter
                                        fromDateTime={
                                            channelProvider.stream_live_at
                                        }
                                    />
                                </Text>
                            )}
                        </Flex>
                    </Fragment>
                ))}
        </Flex>
    )
}

import {
    ChannelProvider,
    ChannelProviderEmbedLive,
    ChannelProviderLiveStatus,
    ChannelProviderToExternalDashboardTitle,
} from '@/features/channel-providers'
import { Box, Flex, Text } from '@mantine/core'
import { YoutubeDashView } from './youtube/youtube-dash-view'

interface Props {
    channelProvider: ChannelProvider
    collapsed?: boolean
}

export function DashboardChannelProvider({
    channelProvider,
    collapsed = false,
}: Props) {
    return (
        <Flex direction="column" gap="0.25rem" h="100%" w={300}>
            <Flex align="center">
                <ChannelProviderToExternalDashboardTitle
                    channelProvider={channelProvider}
                />
                <Box ml="auto">
                    <ChannelProviderLiveStatus
                        channelProvider={channelProvider}
                    />
                </Box>
            </Flex>
            {channelProvider.stream_id && (
                <Text truncate>{channelProvider.stream_title}</Text>
            )}

            <DashView channelProvider={channelProvider} />

            {!collapsed && (
                <>
                    <ChannelProviderEmbedLive
                        channelProvider={channelProvider}
                    />
                </>
            )}
        </Flex>
    )
}

function DashView({ channelProvider }: { channelProvider: ChannelProvider }) {
    switch (channelProvider.provider) {
        case 'youtube':
            return (
                <YoutubeDashView
                    key={channelProvider.provider}
                    channelProvider={channelProvider}
                />
            )
    }
    return null
}

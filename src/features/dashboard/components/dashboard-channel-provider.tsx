import {
    ChannelProvider,
    ChannelProviderDashboardButton,
    ChannelProviderEmbedLive,
    ChannelProviderLiveStatus,
} from '@/features/channel-providers'
import { providers } from '@/types/provider.type'
import { Box, Flex, Paper, Text } from '@mantine/core'
import { TwitchDashView } from './twitch/twitch-dash-view'
import { YoutubeDashView } from './youtube/youtube-dash-view'

interface Props {
    channelProvider: ChannelProvider
}

export function DashboardChannelProvider({ channelProvider }: Props) {
    return (
        <Paper w={300} key={channelProvider.id} withBorder p="0.5rem">
            <Flex direction="column" gap="0.5rem" h="100%">
                <Flex align="center">
                    <Text fw={500}>
                        {providers[channelProvider.provider].name ||
                            channelProvider.provider}
                    </Text>
                    <Box ml="auto">
                        <ChannelProviderLiveStatus
                            channelProvider={channelProvider}
                        />
                    </Box>
                </Flex>
                <Box>
                    <DashView channelProvider={channelProvider} />
                </Box>

                <ChannelProviderEmbedLive channelProvider={channelProvider} />

                <Flex mt="auto">
                    <ChannelProviderDashboardButton
                        channelProvider={channelProvider}
                    />
                </Flex>
            </Flex>
        </Paper>
    )
}

function DashView({ channelProvider }: { channelProvider: ChannelProvider }) {
    switch (channelProvider.provider) {
        case 'twitch':
            return (
                <TwitchDashView
                    key={channelProvider.provider}
                    channelProvider={channelProvider}
                />
            )
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

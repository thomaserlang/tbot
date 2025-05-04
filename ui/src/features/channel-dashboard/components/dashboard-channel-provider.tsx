import {
    ChannelProvider,
    ChannelProviderEmbedLive,
    ChannelProviderLiveStatus,
    ChannelProviderTitle,
    UpdateStreamTitleModal,
} from '@/features/channel-provider'
import { Box, Flex, Text } from '@mantine/core'
import { useDisclosure } from '@mantine/hooks'
import { IconEdit } from '@tabler/icons-react'
import { YoutubeDashView } from './youtube/youtube-dash-view'

interface Props {
    channelProvider: ChannelProvider
    collapsed?: boolean
}

export function DashboardChannelProvider({
    channelProvider,
    collapsed = false,
}: Props) {
    const [opened, { open, close }] = useDisclosure(false)

    return (
        <>
            <Flex direction="column" gap="0.25rem" h="100%" w={300}>
                <Flex align="center">
                    <ChannelProviderTitle channelProvider={channelProvider} />
                    <Box ml="auto">
                        <ChannelProviderLiveStatus
                            channelProvider={channelProvider}
                        />
                    </Box>
                </Flex>

                {channelProvider.stream_id && (
                    <Flex
                        gap="0.25rem"
                        align="center"
                        style={{ cursor: 'pointer' }}
                        onClick={open}
                    >
                        <IconEdit size={18} />
                        <Text truncate>{channelProvider.stream_title}</Text>
                    </Flex>
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

            <UpdateStreamTitleModal
                channelProvider={channelProvider}
                opened={opened}
                onClose={close}
            />
        </>
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

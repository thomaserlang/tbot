import { ViewerCount } from '@/components/viewer-count'
import {
    ChannelProvider,
    ChannelProviderEmbedLive,
    ChannelProviderLiveStatus,
    ChannelProviderTitle,
    UpdateStreamTitleModal,
} from '@/features/channel-provider'
import { ActionIcon, Flex, Text } from '@mantine/core'
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
            <Flex direction="column">
                <Flex align="center">
                    <ChannelProviderTitle channelProvider={channelProvider} />

                    <Flex ml="auto" gap="0.5rem" align="center">
                        <ViewerCount
                            count={channelProvider.stream_viewer_count}
                        />
                        <ChannelProviderLiveStatus
                            channelProvider={channelProvider}
                        />
                    </Flex>
                </Flex>

                {channelProvider.live_stream_id && (
                    <Flex
                        align="center"
                        style={{ cursor: 'pointer' }}
                        onClick={open}
                    >
                        <ActionIcon
                            ml="-0.3rem"
                            size="sm-compact"
                            variant="subtle"
                            color="gray"
                        >
                            <IconEdit size={14} />
                        </ActionIcon>
                        <Text size="sm" truncate>
                            {channelProvider.stream_title}
                        </Text>
                    </Flex>
                )}

                <DashView channelProvider={channelProvider} />

                {!collapsed && (
                    <ChannelProviderEmbedLive
                        channelProvider={channelProvider}
                    />
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

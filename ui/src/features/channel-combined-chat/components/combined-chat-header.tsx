import { TimeCounter } from '@/components/time-counter'
import { ViewerCount } from '@/components/viewer-count'
import { providerInfo } from '@/constants'
import { useCurrentChannel } from '@/features/channel'
import { useGetChannelProviders } from '@/features/channel-provider'
import { ActionIcon, Divider, Flex, Text } from '@mantine/core'
import { IconDotsVertical } from '@tabler/icons-react'
import { Fragment } from 'react/jsx-runtime'
import { ChatMenu } from './chat-menu'

interface Props {
    hideChannelProviders?: boolean
}

export function CombinedChatHeader({ hideChannelProviders }: Props) {
    return (
        <Flex gap="1rem">
            <Text fw={500}>Chat</Text>
            <Flex ml="auto" gap="0.5rem" align="center">
                {!hideChannelProviders && <ChannelProvidersLiveStatus />}

                <ChatMenu>
                    <ActionIcon
                        variant="subtle"
                        size="compact-md"
                        mr="-0.2rem"
                        color="gray"
                    >
                        <IconDotsVertical size={16} />
                    </ActionIcon>
                </ChatMenu>
            </Flex>
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
                        <Flex gap="0.35rem" align="center">
                            {providerInfo[channelProvider.provider].icon}
                            <ViewerCount
                                count={channelProvider.stream_viewer_count}
                            />
                            {channelProvider.stream_live_at && (
                                <Text
                                    size="sm"
                                    c="dimmed"
                                    style={{
                                        fontVariantNumeric: 'tabular-nums',
                                    }}
                                >
                                    <TimeCounter
                                        fromDateTime={
                                            channelProvider.stream_live_at
                                        }
                                    />
                                </Text>
                            )}
                        </Flex>
                        <Divider orientation="vertical" />
                    </Fragment>
                ))}
        </Flex>
    )
}

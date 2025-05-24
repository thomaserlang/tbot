import { TimeCounter } from '@/components/time-counter'
import { ViewerCount } from '@/components/viewer-count'
import { providerInfo } from '@/constants'
import { useCurrentChannel } from '@/features/channel'
import { useGetChannelProviders } from '@/features/channel-provider'
import { ActionIcon, Divider, Flex, ScrollArea, Text } from '@mantine/core'
import { IconDotsVertical } from '@tabler/icons-react'
import dayjs from 'dayjs'
import { Fragment } from 'react/jsx-runtime'
import { ChatMenu } from './chat-menu'

interface Props {
    hideChannelProviders?: boolean
}

export function CombinedChatHeader({ hideChannelProviders }: Props) {
    return (
        <Flex gap="0.75rem" align="center">
            <Text fw={500}>Chat</Text>
            {!hideChannelProviders && (
                <ScrollArea flex={1}>
                    <ChannelProvidersLiveStatus />
                </ScrollArea>
            )}
            <Flex ml="auto" gap="0.75rem" align="center">
                <ChatMenu>
                    <ActionIcon
                        variant="subtle"
                        size="compact-md"
                        color="gray"
                        mr="-0.25rem"
                    >
                        <IconDotsVertical size={18} />
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
        <Flex gap="0.75rem" align="center">
            {data
                ?.filter((f) => f.stream_live)
                .map((channelProvider) => (
                    <Fragment key={channelProvider.id}>
                        <Divider orientation="vertical" />
                        <Flex gap="0.35rem" align="center">
                            {providerInfo[channelProvider.provider].icon?.({
                                size: 18,
                            })}

                            <ViewerCount
                                count={channelProvider.stream_viewer_count}
                            />
                        </Flex>
                    </Fragment>
                ))}
            {(() => {
                if (!data) return null
                const longestLiveProvider = data
                    .filter((f) => f.stream_live && f.stream_live_at)
                    .reduce(
                        (acc, curr) =>
                            !acc ||
                            dayjs(curr.stream_live_at) <
                                dayjs(acc.stream_live_at)
                                ? curr
                                : acc,
                        undefined as (typeof data)[number] | undefined
                    )
                if (!longestLiveProvider?.stream_live_at) return null
                return (
                    <>
                        <Divider orientation="vertical" />
                        <Text
                            size="sm"
                            c="dimmed"
                            style={{
                                fontVariantNumeric: 'tabular-nums',
                            }}
                        >
                            <TimeCounter
                                fromDateTime={
                                    longestLiveProvider.stream_live_at
                                }
                            />
                        </Text>
                    </>
                )
            })()}
        </Flex>
    )
}

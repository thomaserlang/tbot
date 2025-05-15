import { TimeCounter } from '@/components/time-counter'
import { Flex, HoverCard, Text } from '@mantine/core'
import { IconInfoCircleFilled } from '@tabler/icons-react'
import { ChannelProvider } from '../channel-provider.types'

interface Props {
    channelProvider: ChannelProvider
}

export function ChannelProviderLiveStatus({ channelProvider }: Props) {
    if (channelProvider.stream_live) {
        return (
            <Flex gap="0.25rem" align="center">
                <HoverCard width={280}>
                    <HoverCard.Target>
                        <Flex gap="0.25rem" align="center">
                            <Text size="sm">
                                {channelProvider.stream_live_at && (
                                    <TimeCounter
                                        fromDateTime={
                                            channelProvider.stream_live_at
                                        }
                                    />
                                )}
                            </Text>
                            <IconInfoCircleFilled size={20} color="green" />
                        </Flex>
                    </HoverCard.Target>
                    <HoverCard.Dropdown>
                        <Text size="sm">
                            Live status can be a few minutes delayed.
                        </Text>
                    </HoverCard.Dropdown>
                </HoverCard>
            </Flex>
        )
    }

    if (!channelProvider.stream_id) {
        return (
            <Flex gap="0.25rem" align="center">
                <HoverCard width={280}>
                    <HoverCard.Target>
                        <Flex gap="0.25rem" align="center">
                            <Text size="sm">Not ready</Text>
                            <IconInfoCircleFilled
                                size={20}
                                color="var(--mantine-color-yellow-9)"
                            />
                        </Flex>
                    </HoverCard.Target>
                    <HoverCard.Dropdown>
                        <Text size="sm">
                            Click the Configure in Studio button.
                        </Text>
                    </HoverCard.Dropdown>
                </HoverCard>
            </Flex>
        )
    }

    return (
        <Flex gap="0.25rem" align="center">
            <HoverCard width={280}>
                <HoverCard.Target>
                    <Flex gap="0.25rem" align="center">
                        <Text size="sm">
                            {channelProvider.stream_id
                                ? 'Ready to stream'
                                : 'Not ready'}
                        </Text>
                        <IconInfoCircleFilled
                            size={20}
                            color="var(--mantine-color-blue-7)"
                        />
                    </Flex>
                </HoverCard.Target>
                <HoverCard.Dropdown>
                    <Text size="sm">
                        Everything looks ready for you to go live. Live status
                        can be a few minutes delayed.
                    </Text>
                </HoverCard.Dropdown>
            </HoverCard>
        </Flex>
    )
}

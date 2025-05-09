import { providerInfo } from '@/constants'
import { getDashboardUrl } from '@/features/channel-provider'
import { Button, Flex } from '@mantine/core'
import { ChannelProviderDashboardProps } from '../../types'
import { BroadcastScheduleButton } from './broadcast-schedule-button'

export function YoutubeDashView(props: ChannelProviderDashboardProps) {
    if (props.channelProvider.stream_id) return

    return (
        <Flex gap="0.5rem">
            <Button
                component="a"
                href={getDashboardUrl(props.channelProvider)}
                target="_blank"
                leftSection={providerInfo[props.channelProvider.provider].icon}
                variant="default"
                size="xs"
                title="Open YouTube Studio and create a broadcast without a start time"
            >
                Studio
            </Button>

            <BroadcastScheduleButton channelProvider={props.channelProvider} />
        </Flex>
    )
}

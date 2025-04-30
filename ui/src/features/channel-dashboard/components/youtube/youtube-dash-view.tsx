import { providerInfo } from '@/constants'
import { getDashboardUrl } from '@/features/channel-providers'
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
            >
                Dashboard
            </Button>

            <BroadcastScheduleButton channelProvider={props.channelProvider} />
        </Flex>
    )
}

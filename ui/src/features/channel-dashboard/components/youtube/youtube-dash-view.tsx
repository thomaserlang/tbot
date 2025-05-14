import { providerInfo } from '@/constants'
import { getDashboardUrl } from '@/features/channel-provider'
import { Button, Flex } from '@mantine/core'
import { useState } from 'react'
import { ChannelProviderDashboardProps } from '../../types'

export function YoutubeDashView(props: ChannelProviderDashboardProps) {
    const [loading, setLoading] = useState(false)
    if (props.channelProvider.stream_id) return

    return (
        <Flex gap="0.5rem">
            <Button
                component="a"
                href={getDashboardUrl(props.channelProvider)}
                target="_blank"
                onClick={() => {
                    setLoading(true)
                }}
                loading={loading}
                leftSection={providerInfo[props.channelProvider.provider].icon}
                variant="default"
                size="xs"
                title="Open YouTube Studio and create a broadcast without a start time"
            >
                Setup in Studio
            </Button>
        </Flex>
    )
}

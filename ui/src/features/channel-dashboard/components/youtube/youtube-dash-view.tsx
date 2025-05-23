import { providerInfo } from '@/constants'
import { getDashboardUrl } from '@/features/channel-provider'
import { Button, Flex } from '@mantine/core'
import { useState } from 'react'
import { ChannelProviderDashboardProps } from '../../types'

export function YoutubeDashView(props: ChannelProviderDashboardProps) {
    const [loading, setLoading] = useState(false)
    if (props.channelProvider.live_stream_id) return

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
                leftSection={providerInfo[
                    props.channelProvider.provider
                ].icon?.({ size: 18 })}
                variant="default"
                size="xs"
            >
                Configure in Studio
            </Button>
        </Flex>
    )
}

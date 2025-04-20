import { providers } from '@/types/provider.type'
import { Flex, Text } from '@mantine/core'
import { ChannelProvider } from '../channel-provider.types'
import { ChannelProviderContextMenu } from './channel-provider-context-menu'

interface Props {
    channelProvider: ChannelProvider
}

export function ChannelProviderTitle({ channelProvider }: Props) {
    if (!providers[channelProvider.provider].dashboard_url)
        return (
            <Text fw={500}>
                {providers[channelProvider.provider].name ||
                    channelProvider.provider}
            </Text>
        )
    return (
        <Flex gap="0.25rem" align="center">
            <ChannelProviderContextMenu channelProvider={channelProvider} />
            <Text component="a" fw={500} target="_blank">
                {providers[channelProvider.provider].name ||
                    channelProvider.provider}
            </Text>
        </Flex>
    )
}

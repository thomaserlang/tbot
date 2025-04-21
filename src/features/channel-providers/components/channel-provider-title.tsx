import { providerInfo } from '@/constants'
import { Flex, Text } from '@mantine/core'
import { ChannelProvider } from '../channel-provider.types'
import { ChannelProviderContextMenu } from './channel-provider-context-menu'

interface Props {
    channelProvider: ChannelProvider
}

export function ChannelProviderTitle({ channelProvider }: Props) {
    if (!providerInfo[channelProvider.provider].dashboard_url)
        return (
            <Text fw={500}>
                {providerInfo[channelProvider.provider].name ||
                    channelProvider.provider}
            </Text>
        )
    return (
        <Flex gap="0.25rem" align="center">
            <ChannelProviderContextMenu channelProvider={channelProvider} />
            <Text component="a" fw={500} target="_blank">
                {providerInfo[channelProvider.provider].name ||
                    channelProvider.provider}
            </Text>
        </Flex>
    )
}

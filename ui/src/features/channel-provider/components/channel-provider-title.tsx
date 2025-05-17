import { providerInfo } from '@/constants'
import { Box, Flex, Text } from '@mantine/core'
import { ChannelProvider } from '../channel-provider.types'
import { ChannelProviderContextMenu } from './channel-provider-context-menu'

interface Props {
    channelProvider: ChannelProvider
}

export function ChannelProviderTitle({ channelProvider }: Props) {
    if (!providerInfo[channelProvider.provider].dashboardUrl)
        return (
            <Text fw={500}>
                {providerInfo[channelProvider.provider].name ||
                    channelProvider.provider}
            </Text>
        )
    return (
        <Flex gap="0.1rem" align="center">
            <Box ml="-0.35rem" mt="0.1rem">
                <ChannelProviderContextMenu channelProvider={channelProvider} />
            </Box>

            <Text component="a" size="sm" fw={500} target="_blank">
                {providerInfo[channelProvider.provider].name ||
                    channelProvider.provider}
            </Text>
        </Flex>
    )
}

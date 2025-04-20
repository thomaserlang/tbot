import { providers } from '@/types/provider.type'
import { Button, Flex, Text } from '@mantine/core'
import { IconExternalLink } from '@tabler/icons-react'
import { ChannelProvider } from '../channel-provider.types'

interface Props {
    channelProvider: ChannelProvider
}

export function ChannelProviderToExternalDashboardButton({
    channelProvider,
}: Props) {
    if (!providers[channelProvider.provider].dashboard_url) return

    return (
        <Button
            component={'a'}
            href={getUrl(channelProvider)}
            target="_blank"
            rightSection={<IconExternalLink size={16} />}
            color={providers[channelProvider.provider].color}
        >
            Dashboard
        </Button>
    )
}

export function ChannelProviderToExternalDashboardTitle({
    channelProvider,
}: Props) {
    if (!providers[channelProvider.provider].dashboard_url)
        return (
            <Text fw={500}>
                {providers[channelProvider.provider].name ||
                    channelProvider.provider}
            </Text>
        )
    return (
        <Flex gap="0.25rem" align="center">
            <Text
                component="a"
                fw={500}
                href={getUrl(channelProvider)}
                target="_blank"
            >
                {providers[channelProvider.provider].name ||
                    channelProvider.provider}
            </Text>

            <IconExternalLink size={16} />
        </Flex>
    )
}

function getUrl(channelProvider: ChannelProvider) {
    if (
        channelProvider.stream_id &&
        providers[channelProvider.provider].broadcast_edit_url
    )
        return providers[channelProvider.provider].broadcast_edit_url?.replace(
            /{([^{}]+)}/g,
            (_, key) => (channelProvider[key] as string) || ''
        )
    return providers[channelProvider.provider].dashboard_url?.replace(
        /{([^{}]+)}/g,
        (_, key) => (channelProvider[key] as string) || ''
    )
}

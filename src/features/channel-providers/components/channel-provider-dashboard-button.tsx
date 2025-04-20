import { providers } from '@/types/provider.type'
import { Button } from '@mantine/core'
import { IconExternalLink } from '@tabler/icons-react'
import { ChannelProvider } from '../channel-provider.types'

interface Props {
    channelProvider: ChannelProvider
}

export function ChannelProviderDashboardButton({ channelProvider }: Props) {
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

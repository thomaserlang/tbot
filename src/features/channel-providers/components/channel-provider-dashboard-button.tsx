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
            href={providers[channelProvider.provider].dashboard_url?.replace(
                /{([^{}]+)}/g,
                (_, key) => (channelProvider[key] as string) || ''
            )}
            target="_blank"
            rightSection={<IconExternalLink size={16} />}
            color={providers[channelProvider.provider].color}
        >
            Dashboard
        </Button>
    )
}

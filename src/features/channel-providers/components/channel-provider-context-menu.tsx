import { providers } from '@/types/provider.type'
import { ActionIcon, Menu } from '@mantine/core'
import { IconDotsVertical, IconExternalLink } from '@tabler/icons-react'
import { ChannelProvider } from '../channel-provider.types'

interface Props {
    channelProvider: ChannelProvider
}

export function ChannelProviderContextMenu({ channelProvider }: Props) {
    return (
        <Menu width={200}>
            <Menu.Target>
                <ActionIcon size="sm-compact" variant="subtle" color="gray">
                    <IconDotsVertical size={16} />
                </ActionIcon>
            </Menu.Target>
            <Menu.Dropdown>
                <Menu.Item
                    component="a"
                    leftSection={<IconExternalLink size={18} />}
                    href={getUrl(channelProvider)}
                    target="_blank"
                >
                    {providers[channelProvider.provider].name} Dashboard
                </Menu.Item>
            </Menu.Dropdown>
        </Menu>
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

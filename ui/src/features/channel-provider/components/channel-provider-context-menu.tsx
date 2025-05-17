import { providerInfo } from '@/constants'
import { ActionIcon, Menu } from '@mantine/core'
import { IconDotsVertical } from '@tabler/icons-react'
import { ChannelProvider } from '../channel-provider.types'
import { getDashboardUrl } from '../utils'

interface Props {
    channelProvider: ChannelProvider
}

export function ChannelProviderContextMenu({ channelProvider }: Props) {
    return (
        <Menu width={200}>
            <Menu.Target>
                <ActionIcon size="sm-compact" variant="subtle" color="gray">
                    <IconDotsVertical size={14} />
                </ActionIcon>
            </Menu.Target>
            <Menu.Dropdown>
                <Menu.Item
                    component="a"
                    leftSection={providerInfo[channelProvider.provider].icon}
                    href={getDashboardUrl(channelProvider)}
                    target="_blank"
                >
                    Dashboard
                </Menu.Item>
            </Menu.Dropdown>
        </Menu>
    )
}

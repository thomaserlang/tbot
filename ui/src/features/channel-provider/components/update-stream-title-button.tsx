import { providerInfo } from '@/constants/providers-info.constants'
import { ChannelId } from '@/features/channel/types'
import { Button, Menu } from '@mantine/core'
import { IconCaretDownFilled } from '@tabler/icons-react'
import { useState } from 'react'
import { useGetChannelProviders } from '../api/channel-providers.api'
import { ChannelProvider } from '../channel-provider.types'
import { UpdateStreamTitleModal } from './update-stream-title-modal'

interface Props {
    channelId: ChannelId
}

export function UpdateStreamTitleButton({ channelId }: Props) {
    const channelProviders = useGetChannelProviders({ channelId })
    const [channelProvider, setChannelProvider] =
        useState<ChannelProvider | null>(null)

    return (
        <>
            <Menu shadow="md" width={200}>
                <Menu.Target>
                    <Button
                        rightSection={<IconCaretDownFilled />}
                        variant="light"
                    >
                        Update Title
                    </Button>
                </Menu.Target>
                <Menu.Dropdown>
                    {channelProviders.data
                        ?.filter(
                            (p) => providerInfo[p.provider].streamTitleMaxLength
                        )
                        .map((p) => (
                            <Menu.Item
                                key={p.id}
                                onClick={() => {
                                    setChannelProvider(p)
                                }}
                            >
                                {providerInfo[p.provider].name}
                            </Menu.Item>
                        ))}
                </Menu.Dropdown>
            </Menu>
            {channelProvider && (
                <UpdateStreamTitleModal
                    channelProvider={channelProvider}
                    onClose={() => setChannelProvider(null)}
                    opened={!!channelProvider}
                />
            )}
        </>
    )
}

import { providerInfo } from '@/constants'
import { ChannelId } from '@/features/channel'
import { toastError } from '@/utils/toast'
import { Button, Menu } from '@mantine/core'
import { IconPlus } from '@tabler/icons-react'
import { useGetChannelProviderConnectUrl } from '../api/channel-provider.api'

interface Props {
    channelId: ChannelId
}

export function AddChannelProviderButton({ channelId }: Props) {
    const add = useGetChannelProviderConnectUrl({
        onSuccess: ({ url }) => {
            window.location.href = url
        },
        onError: (error) => {
            toastError(error)
        },
    })

    return (
        <Menu width={200}>
            <Menu.Target>
                <Button
                    ml="auto"
                    variant="light"
                    loading={add.isPending}
                    leftSection={<IconPlus size={14} />}
                >
                    Add Provider
                </Button>
            </Menu.Target>

            <Menu.Dropdown>
                {Object.values(providerInfo).map((provider) => (
                    <Menu.Item
                        key={provider.key}
                        onClick={() => {
                            add.mutate({
                                channelId,
                                provider: provider.key,
                            })
                        }}
                    >
                        {provider.name}
                    </Menu.Item>
                ))}
            </Menu.Dropdown>
        </Menu>
    )
}

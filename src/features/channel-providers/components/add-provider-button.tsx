import { ChannelId } from '@/features/channel'
import { Provider } from '@/types/provider.type'
import { toastError } from '@/utils/toast'
import { Button, Menu } from '@mantine/core'
import { IconPlus } from '@tabler/icons-react'
import { useGetProviderConnectUrl } from '../provider.api'
import { channelProviderLabels } from '../provider.types'

interface Props {
    channelId: ChannelId
}

export function AddProviderButton({ channelId }: Props) {
    const add = useGetProviderConnectUrl({
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
                {Object.keys(channelProviderLabels).map((t) => (
                    <Menu.Item
                        key={t}
                        onClick={() => {
                            add.mutate({
                                channelId,
                                provider: t as Provider,
                            })
                        }}
                    >
                        {channelProviderLabels[t]}
                    </Menu.Item>
                ))}
            </Menu.Dropdown>
        </Menu>
    )
}

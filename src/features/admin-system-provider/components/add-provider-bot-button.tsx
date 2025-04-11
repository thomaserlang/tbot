import { providerBotLabels } from '@/features/provider-bot/provider-bot.types'
import { Provider } from '@/types/provider.type'
import { toastError } from '@/utils/toast'
import { Button, Menu } from '@mantine/core'
import { IconPlus } from '@tabler/icons-react'
import { useGetSystemProviderBotConnectUrl } from '../provider-bot.api'

export function AddProviderButton() {
    const add = useGetSystemProviderBotConnectUrl({
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
                    Add Provider Bot
                </Button>
            </Menu.Target>

            <Menu.Dropdown>
                {Object.keys(providerBotLabels).map((t) => (
                    <Menu.Item
                        key={t}
                        onClick={() => {
                            add.mutate({
                                provider: t as Provider,
                            })
                        }}
                    >
                        {providerBotLabels[t]}
                    </Menu.Item>
                ))}
            </Menu.Dropdown>
        </Menu>
    )
}

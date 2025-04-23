import { providerInfo } from '@/constants'
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
                {Object.values(providerInfo)
                    .filter((t) => t.systemBot)
                    .map((t) => (
                        <Menu.Item
                            key={t.key}
                            onClick={() => {
                                add.mutate({
                                    provider: t.key,
                                })
                            }}
                        >
                            {t.name}
                        </Menu.Item>
                    ))}
            </Menu.Dropdown>
        </Menu>
    )
}

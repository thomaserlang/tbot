import { toastError, toastSuccess } from '@/utils/toast'
import { Button, Flex, Text } from '@mantine/core'
import { openConfirmModal } from '@mantine/modals'
import {
    useDisconnectChannelProviderBot,
    useGetChannelProviderConnectBotUrl,
} from '../channel-provider.api'
import { ChannelProvider } from '../channel-provider.types'

interface Props {
    provider: ChannelProvider
}

export function BotButtonAction({ provider }: Props) {
    const connectBotUrl = useGetChannelProviderConnectBotUrl({
        onSuccess: ({ url }) => {
            window.location.href = url
        },
        onError: (error) => {
            toastError(error)
        },
    })

    const disconnectBotUrl = useDisconnectChannelProviderBot({
        onSuccess: () => {
            toastSuccess('Bot disconnected')
        },
        onError: (error) => {
            toastError(error)
        },
    })

    return (
        <Flex gap="1rem">
            {provider.bot_provider && (
                <Button
                    color="red"
                    loading={disconnectBotUrl.isPending}
                    onClick={() => {
                        openConfirmModal({
                            title: 'Disconnect bot',
                            children: (
                                <Text>
                                    Are you sure you want to disconnect the bot?
                                </Text>
                            ),
                            confirmProps: { color: 'red' },
                            labels: {
                                confirm: 'Disconnect',
                                cancel: 'Cancel',
                            },
                            onConfirm: () => {
                                disconnectBotUrl.mutate({
                                    channelId: provider.channel_id,
                                    providerId: provider.id,
                                })
                            },
                        })
                    }}
                >
                    Disconnect bot {provider.bot_provider.name}
                </Button>
            )}

            {!provider.bot_provider && (
                <Button
                    color="blue"
                    loading={connectBotUrl.isPending}
                    onClick={() => {
                        connectBotUrl.mutate({
                            channelId: provider.channel_id,
                            provider: provider.provider,
                        })
                    }}
                >
                    Connect bot
                </Button>
            )}

            {provider.bot_provider?.scope_needed && (
                <Button
                    color="blue"
                    loading={connectBotUrl.isPending}
                    onClick={() => {
                        connectBotUrl.mutate({
                            channelId: provider.channel_id,
                            provider: provider.provider,
                        })
                    }}
                >
                    Extra permissions needed
                </Button>
            )}
        </Flex>
    )
}

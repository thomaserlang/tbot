import { ProviderBot } from '@/features/provider-bot/provider-bot.types'
import { toastError, toastSuccess } from '@/utils/toast'
import { Button, Flex, Text } from '@mantine/core'
import { openConfirmModal } from '@mantine/modals'
import {
    useDeleteSystemProviderBot,
    useGetSystemProviderBotConnectUrl,
} from '../provider-bot.api'

interface Props {
    provider: ProviderBot
    onDeleted?: () => void
}

export function ButtonAction({ provider, onDeleted }: Props) {
    const connectUrl = useGetSystemProviderBotConnectUrl({
        onSuccess: ({ url }) => {
            window.location.href = url
        },
        onError: (error) => {
            toastError(error)
        },
    })

    const deleteProvider = useDeleteSystemProviderBot({
        onSuccess: () => {
            toastSuccess('Provider deleted')
            onDeleted?.()
        },
        onError: (error) => {
            toastError(error)
        },
    })

    return (
        <Flex gap="1rem">
            {provider.scope_needed && (
                <Button
                    color="blue"
                    loading={connectUrl.isPending}
                    onClick={() => {
                        connectUrl.mutate({
                            provider: provider.provider,
                        })
                    }}
                >
                    Extra permissions needed
                </Button>
            )}

            <Button
                color="red"
                loading={deleteProvider.isPending}
                onClick={() => {
                    openConfirmModal({
                        title: 'Delete provider bot',
                        children: (
                            <Text>
                                Are you sure you want to delete this provider
                                bot?
                            </Text>
                        ),
                        confirmProps: { color: 'red' },
                        labels: { confirm: 'Delete', cancel: 'Cancel' },
                        onConfirm: () => {
                            deleteProvider.mutate({
                                provider: provider.provider,
                            })
                        },
                    })
                }}
            >
                Delete
            </Button>
        </Flex>
    )
}

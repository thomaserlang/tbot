import { toastError, toastSuccess } from '@/utils/toast'
import { Button, Flex, Text } from '@mantine/core'
import { openConfirmModal } from '@mantine/modals'
import { useDeleteProvider, useGetProviderConnectUrl } from '../provider.api'
import { ChannelProvider } from '../provider.types'

interface Props {
    provider: ChannelProvider
    onDeleted?: () => void
}

export function ButtonAction({ provider, onDeleted }: Props) {
    const connectUrl = useGetProviderConnectUrl({
        onSuccess: ({ url }) => {
            window.location.href = url
        },
        onError: (error) => {
            toastError(error)
        },
    })

    const deleteProvider = useDeleteProvider({
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
                            channelId: provider.channel_id,
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
                        title: 'Delete provider',
                        children: (
                            <Text>
                                Are you sure you want to delete this provider?
                            </Text>
                        ),
                        confirmProps: { color: 'red' },
                        labels: { confirm: 'Delete', cancel: 'Cancel' },
                        onConfirm: () => {
                            deleteProvider.mutate({
                                channelId: provider.channel_id,
                                providerId: provider.id,
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

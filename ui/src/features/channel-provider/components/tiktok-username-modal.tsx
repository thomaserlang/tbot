import { ErrorBox } from '@/components/error-box'
import { ChannelId } from '@/features/channel/types'
import { api } from '@/utils/api'
import { toastSuccess } from '@/utils/toast'
import { Button, Flex, Modal, TextInput } from '@mantine/core'
import { useForm } from '@mantine/form'
import { IconAt } from '@tabler/icons-react'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { getChannelProvidersQueryKey } from '../api/channel-providers.api'
import { ChannelProvider } from '../channel-provider.types'

interface Props {
    channelId: ChannelId
    opened: boolean
    onClose: () => void
    onSaved?: (data: ChannelProvider) => void
}

export function TiktokUsernameModal({
    channelId,
    opened,
    onClose,
    onSaved,
}: Props) {
    const queryClient = useQueryClient()
    const save = useMutation({
        mutationFn: async (username: string) => {
            const r = await api.post<ChannelProvider>(
                `/api/2/channels/${channelId}/register-provider/tiktok`,
                {
                    username,
                }
            )
            return r.data
        },
        onSuccess: (data) => {
            queryClient.setQueryData(
                getChannelProvidersQueryKey(channelId),
                (oldData: ChannelProvider[]) => [data, ...(oldData || [])]
            )
            queryClient.invalidateQueries({
                queryKey: getChannelProvidersQueryKey(channelId),
            })
            toastSuccess('Tiktok saved')
            onSaved?.(data)
            onClose()
        },
    })
    const form = useForm({
        initialValues: {
            username: '',
        },
    })

    return (
        <Modal opened={opened} onClose={onClose} title="Tiktok Username">
            {opened && (
                <form
                    onSubmit={form.onSubmit((values) => {
                        save.mutate(values.username)
                    })}
                >
                    <Flex gap="1rem" direction="column">
                        <TextInput
                            leftSection={<IconAt />}
                            size="lg"
                            placeholder="TikTok username"
                            data-autofocus
                            key={form.key('username')}
                            {...form.getInputProps('username')}
                        />

                        {save.error && <ErrorBox errorObj={save.error} />}

                        <Flex>
                            <Button
                                ml="auto"
                                type="submit"
                                loading={save.isPending}
                            >
                                Save
                            </Button>
                        </Flex>
                    </Flex>
                </form>
            )}
        </Modal>
    )
}

import { ChannelId, useDeleteChannel } from '@/features/channel'
import { toastError, toastSuccess } from '@/utils/toast'
import { Box, Button, Flex, Text, TextInput } from '@mantine/core'
import { useForm } from '@mantine/form'
import { useNavigate } from 'react-router-dom'

interface Props {
    channelId: ChannelId
}

export function DeleteChannelConfirm({ channelId }: Props) {
    const navigate = useNavigate()
    const deleteChannel = useDeleteChannel({
        onSuccess: () => {
            navigate('/channels')
            toastSuccess('Channel deleted successfully')
        },
        onError: (error) => {
            toastError(error)
        },
    })
    const form = useForm({
        initialValues: {
            channelName: '',
        },
    })

    return (
        <form
            onSubmit={form.onSubmit((values) => {
                deleteChannel.mutate({
                    channelId,
                    channelName: values.channelName,
                })
            })}
        >
            <Flex direction="column" gap="1rem">
                <Box>
                    <Text>Are you sure you want to delete this channel?</Text>
                    <Text>This is an irreversible action, please be sure.</Text>
                </Box>

                <Box>
                    <Text>To confirm, type the channel name:</Text>
                    <TextInput
                        data-autofocus
                        key={form.key('channelName')}
                        {...form.getInputProps('channelName')}
                        placeholder="Channel name"
                    />
                </Box>

                <Flex>
                    <Button
                        color="red"
                        ml="auto"
                        loading={deleteChannel.isPending}
                        type="submit"
                    >
                        Delete this channel
                    </Button>
                </Flex>
            </Flex>
        </form>
    )
}

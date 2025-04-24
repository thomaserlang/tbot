import { useDeleteCurrentUser } from '@/components/current-user'
import { setAccessToken } from '@/utils/api'
import { toastError, toastSuccess } from '@/utils/toast'
import { Box, Button, Flex, Text, TextInput } from '@mantine/core'
import { useForm } from '@mantine/form'

export function DeleteUserConfirm() {
    const deleteUser = useDeleteCurrentUser({
        onSuccess: () => {
            setAccessToken('')
            window.location.href = '/'
            toastSuccess(
                'Your user account has been deleted successfully, bye!'
            )
        },
        onError: (error) => {
            toastError(error)
        },
    })
    const form = useForm({
        initialValues: {
            username: '',
        },
    })

    return (
        <form
            onSubmit={form.onSubmit((values) => {
                deleteUser.mutate({
                    username: values.username,
                })
            })}
        >
            <Flex direction="column" gap="1rem">
                <Box>
                    <Text>
                        Are you sure you want to delete your user account?
                    </Text>
                    <Text>This is an irreversible action, please be sure.</Text>
                </Box>

                <Box>
                    <Text>To confirm, type your username:</Text>
                    <TextInput
                        data-autofocus
                        key={form.key('username')}
                        {...form.getInputProps('username')}
                        placeholder="Username"
                    />
                </Box>

                <Flex>
                    <Button
                        color="red"
                        ml="auto"
                        loading={deleteUser.isPending}
                        type="submit"
                    >
                        Delete user account
                    </Button>
                </Flex>
            </Flex>
        </form>
    )
}

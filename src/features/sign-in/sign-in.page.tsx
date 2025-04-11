import { APP_TITLE } from '@/constants'
import { toastError } from '@/utils/toast'
import { Button, Container, Flex, Title } from '@mantine/core'
import { IconBrandTwitch } from '@tabler/icons-react'
import { useGetSignInUrl } from './sign-in.api'

export function Component() {
    const signInUrl = useGetSignInUrl({
        onSuccess: ({ url }) => {
            window.location.href = url
        },
        onError: (error) => {
            toastError(error)
        },
    })

    return (
        <Container size="xs">
            <Flex
                gap="1rem"
                h="10rem"
                justify="center"
                align="center"
                direction="column"
            >
                <Title>{APP_TITLE}</Title>
                <Button
                    bg="#6441A5"
                    leftSection={<IconBrandTwitch />}
                    loading={signInUrl.isSuccess}
                    onClick={() => {
                        signInUrl.mutate({
                            provider: 'twitch',
                        })
                    }}
                >
                    Sign in with Twitch
                </Button>
            </Flex>
        </Container>
    )
}

import { Logo } from '@/components/logo'
import { providerInfo } from '@/constants'
import { toastError } from '@/utils/toast'
import { Button, Container, Flex, Paper, Title } from '@mantine/core'
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
        <>
            <title>Sign in - HEIMRA</title>
            <Container size="xs" mt="3rem">
                <Flex gap="1rem" direction="column" align="center">
                    <Logo width="10rem" />
                    <Paper withBorder p="1rem">
                        <Title order={2}>Sign in</Title>
                        <Flex
                            gap="1rem"
                            h="10rem"
                            justify="center"
                            align="center"
                            direction="column"
                        >
                            {Object.values(providerInfo)
                                .filter((f) => f.signinProvider)
                                .map((provider) => (
                                    <Button
                                        key={provider.key}
                                        bg={provider.color}
                                        leftSection={provider.icon}
                                        loading={signInUrl.isSuccess}
                                        onClick={() => {
                                            signInUrl.mutate({
                                                provider: provider.key,
                                            })
                                        }}
                                        w={250}
                                    >
                                        Sign in with {provider.name}
                                    </Button>
                                ))}
                        </Flex>
                    </Paper>
                </Flex>
            </Container>
        </>
    )
}

import { Logo } from '@/components/logo'
import { providerInfo } from '@/constants'
import { toastError } from '@/utils/toast'
import { Box, Button, Container, Flex, Paper } from '@mantine/core'
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
            <title>Sign in - Synchra</title>
            <Container mt="3rem">
                <Flex gap="1rem" direction="column" align="center">
                    <Box h={50}>
                        <Logo width="10rem" />
                    </Box>
                    <Paper withBorder p="1rem">
                        <Flex
                            gap="1rem"
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
                                        loading={signInUrl.isPending}
                                        onClick={() => {
                                            signInUrl.mutate({
                                                provider: provider.key,
                                            })
                                        }}
                                        w="100%"
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

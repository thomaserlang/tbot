import { Logo } from '@/components/logo'
import { providerInfo } from '@/constants'
import { toastError } from '@/utils/toast'
import {
    Anchor,
    Box,
    Button,
    Center,
    Container,
    Flex,
    Paper,
    Text,
} from '@mantine/core'
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
                        <Logo />
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
                                        leftSection={provider.icon?.({
                                            size: 18,
                                        })}
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
                <Center mt="1rem">
                    <Flex gap="0.5rem">
                        <Anchor
                            size="sm"
                            c="dimmed"
                            href="https://synchra.net/privacy"
                            target="_blank"
                        >
                            Privacy Policy
                        </Anchor>
                        <Text size="sm" c="dimmed">
                            •
                        </Text>
                        <Anchor
                            size="sm"
                            c="dimmed"
                            href="https://synchra.net/terms"
                            target="_blank"
                        >
                            Terms of Use
                        </Anchor>
                    </Flex>
                </Center>
            </Container>
        </>
    )
}

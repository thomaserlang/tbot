import { APP_TITLE } from '@/constants'
import { Button, Container, Flex, Title } from '@mantine/core'
import { IconBrandTwitch } from '@tabler/icons-react'
import { useState } from 'react'

export function Component() {
    const [loading, setLoading] = useState('')
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
                    component="a"
                    href={`/api/2/twitch/sign-in`}
                    bg="#6441A5"
                    leftSection={<IconBrandTwitch />}
                    loading={loading === 'twitch'}
                    onClick={() => {
                        setLoading('twitch')
                    }}
                >
                    Sign in with Twitch
                </Button>
            </Flex>
        </Container>
    )
}

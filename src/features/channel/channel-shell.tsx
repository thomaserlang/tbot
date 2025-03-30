import { Anchor, AppShell, Burger, Flex, Paper, Text } from '@mantine/core'
import { useDisclosure } from '@mantine/hooks'
import { ReactNode, useEffect } from 'react'
import { Link, useLocation } from 'react-router'

import { CurrentUserCard } from '@/components/current-user'
import { CurrentChannelCard } from './components/current-channel-card'
import { CurrentChannelProvider } from './current-channel.provider'

export function ChannelShell({ children }: { children: ReactNode }) {
    const [opened, { toggle, close }] = useDisclosure()
    const { pathname } = useLocation()

    useEffect(() => {
        close()
    }, [pathname])

    return (
        <CurrentChannelProvider>
            <AppShell
                navbar={{
                    width: 250,
                    breakpoint: 'md',
                    collapsed: { mobile: !opened },
                }}
                header={{ height: 50 }}
                padding="md"
            >
                <AppShell.Header>
                    <Flex
                        gap="2rem"
                        h="100%"
                        align="center"
                        p="0.25rem"
                        pl="1rem"
                    >
                        <Burger
                            opened={opened}
                            onClick={toggle}
                            hiddenFrom="md"
                            size="sm"
                        />

                        <Anchor
                            className="logo"
                            size="xl"
                            component={Link}
                            to="/"
                        >
                            <Text fw={700}>TBot</Text>
                        </Anchor>

                        <Flex gap="0.5rem" align="center" ml="auto">
                            <Paper withBorder p="0.25rem" radius="md">
                                <CurrentChannelCard nameFw={500} w={200} />
                            </Paper>
                        </Flex>

                        <Flex ml="auto" mr="0.5rem">
                            <CurrentUserCard />
                        </Flex>
                    </Flex>
                </AppShell.Header>

                <AppShell.Navbar>NAV</AppShell.Navbar>

                <AppShell.Main>{children}</AppShell.Main>
            </AppShell>
        </CurrentChannelProvider>
    )
}

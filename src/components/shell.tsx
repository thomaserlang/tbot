import { Anchor, AppShell, Burger, Flex } from '@mantine/core'
import { useDisclosure } from '@mantine/hooks'
import { ReactNode, useEffect } from 'react'
import { Link, useLocation } from 'react-router'
import { CurrentUserCard, CurrentUserProvider } from './current-user'

export function Shell({ children }: { children: ReactNode }) {
    const [opened, { toggle, close }] = useDisclosure()
    const { pathname } = useLocation()

    useEffect(() => {
        close()
    }, [pathname])

    return (
        <AppShell
            navbar={{
                width: 250,
                breakpoint: 'md',
                collapsed: { mobile: !opened },
            }}
            header={{ height: 50 }}
            padding="md"
        >
            <CurrentUserProvider>
                <AppShell.Header>
                    <Flex
                        gap="1rem"
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

                        <Anchor className="logo" component={Link} to="/">
                            TBOT
                        </Anchor>

                        <Flex ml="auto" align="center" gap="1rem" mr="0.5rem">
                            <CurrentUserCard />
                        </Flex>
                    </Flex>
                </AppShell.Header>

                <AppShell.Navbar>NAV</AppShell.Navbar>

                <AppShell.Main>{children}</AppShell.Main>
            </CurrentUserProvider>
        </AppShell>
    )
}

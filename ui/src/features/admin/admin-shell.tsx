import { Anchor, AppShell, Burger, Flex, Text } from '@mantine/core'
import { useDisclosure } from '@mantine/hooks'
import { ReactNode, useEffect } from 'react'
import { Link, useLocation } from 'react-router'

import { CurrentUserCard } from '@/components/current-user'
import { APP_TITLE } from '@/constants'
import { AdminNavbar } from './admin-navbar'

export function AdminShell({ children }: { children: ReactNode }) {
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
            <AppShell.Header>
                <Flex
                    gap="0.5rem"
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

                    <Anchor className="logo" size="xl" component={Link} to="/">
                        <Text fw={700}>{APP_TITLE}</Text>
                    </Anchor>

                    <Text fw={700} size="xl">
                        Admin
                    </Text>

                    <Flex ml="auto" mr="0.5rem">
                        <CurrentUserCard />
                    </Flex>
                </Flex>
            </AppShell.Header>

            <AppShell.Navbar>
                <AdminNavbar />
            </AppShell.Navbar>

            <AppShell.Main>{children}</AppShell.Main>
        </AppShell>
    )
}

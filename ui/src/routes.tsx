import { ErrorBox } from '@/components/error-box'
import { Anchor, Center, Container, Text, Title } from '@mantine/core'
import {
    createBrowserRouter,
    isRouteErrorResponse,
    Outlet,
    RouteObject,
    useRouteError,
} from 'react-router-dom'
import { QueryParamProvider } from 'use-query-params'
import { ReactRouter6Adapter } from 'use-query-params/adapters/react-router-6'
import { CurrentUserProvider } from './components/current-user'
import { AdminShell } from './features/admin/admin-shell'
import { ChannelShell } from './features/channel/channel-shell'

import { Logo } from './components/logo'

const protectedRoutes: RouteObject[] = [
    {
        path: '/channels',
        lazy: () => import('./features/channel/channels.page'),
    },
    {
        path: '/channel-invite/:channelUserInviteId',
        lazy: () =>
            import(
                './features/channel-user-access/channel-user-invite-accept.page'
            ),
    },
    {
        path: '/channels/:channelId',
        element: (
            <ChannelShell>
                <Outlet />
            </ChannelShell>
        ),
        ErrorBoundary: () => {
            const error = useRouteError()
            return (
                <ChannelShell>
                    <Container pt="1rem">
                        <ErrorBox errorObj={error} />
                    </Container>
                </ChannelShell>
            )
        },
        children: [
            {
                path: '',
                lazy: () =>
                    import('./features/channel-dashboard/dashboard.page'),
            },
            {
                path: 'settings',
                lazy: () =>
                    import('./features/channel-settings/channel-settings.page'),
            },
            {
                path: 'providers',
                lazy: () =>
                    import(
                        './features/channel-providers/channel-providers.page'
                    ),
            },
            {
                path: 'providers/:providerId',
                lazy: () =>
                    import(
                        './features/channel-providers/channel-providers.page'
                    ),
            },
            {
                path: 'commands',
                lazy: () => import('./features/channel-commands/commands.page'),
            },
            {
                path: 'commands/:commandId',
                lazy: () => import('./features/channel-commands/commands.page'),
            },
            {
                path: 'timers',
                lazy: () => import('./features/channel-timers/timers.page'),
            },
            {
                path: 'timers/:timerId',
                lazy: () => import('./features/channel-timers/timers.page'),
            },
            {
                path: 'chat-filters',
                lazy: () =>
                    import('./features/channel-chat-filters/filters.page'),
            },
            {
                path: 'chat-filters/:filterId',
                lazy: () =>
                    import('./features/channel-chat-filters/filters.page'),
            },
            {
                path: 'combined-chat',
                lazy: () =>
                    import(
                        './features/channel-combined-chat/combined-chat.page'
                    ),
            },
            {
                path: 'user-access',
                lazy: () =>
                    import(
                        './features/channel-user-access/channel-user-access.page'
                    ),
            },
            {
                path: 'gambling/point-settings',
                lazy: () =>
                    import(
                        './features/channel-points/channel-point-settings.page'
                    ),
            },
            {
                path: 'gambling/roulette-settings',
                lazy: () =>
                    import(
                        './features/channel-gambling-roulette/roulette-settings.page'
                    ),
            },
            {
                path: 'gambling/slots-settings',
                lazy: () =>
                    import(
                        './features/channel-gambling-slots/slots-settings.page'
                    ),
            },
        ],
    },
    {
        path: '/admin',
        element: (
            <AdminShell>
                <Outlet />
            </AdminShell>
        ),
        ErrorBoundary: () => {
            const error = useRouteError()
            return (
                <AdminShell>
                    <Container pt="1rem">
                        <ErrorBox errorObj={error} />
                    </Container>
                </AdminShell>
            )
        },
        children: [
            {
                path: 'system-provider-bots',
                lazy: () =>
                    import(
                        './features/admin-system-provider/system-provider-bots.page'
                    ),
            },
            {
                path: 'system-provider-bots/:provider',
                lazy: () =>
                    import(
                        './features/admin-system-provider/system-provider-bots.page'
                    ),
            },
        ],
    },
]

const publicRoutes: RouteObject[] = [
    {
        path: '',
        lazy: () => import('./features/landing-page/landing.page'),
    },
    {
        path: '/sign-in',
        lazy: () => import('./features/sign-in/sign-in.page'),
    },
    {
        path: '/sign-in/success',
        lazy: () => import('./features/sign-in/sign-in-success.page'),
    },
]

export const router = createBrowserRouter([
    {
        ErrorBoundary: () => {
            const error = useRouteError()
            if (isRouteErrorResponse(error)) {
                return (
                    <Container size="xs" pt="1rem">
                        <Center mb="2rem">
                            <Logo width="35rem" />
                        </Center>
                        <Title order={1}>{error.status}</Title>
                        <Text mb="1rem">{error.statusText}</Text>
                        <Anchor>Go back</Anchor>
                    </Container>
                )
            }
            return (
                <Container pt="1rem">
                    <Center mb="2rem">
                        <Logo width="35rem" />
                    </Center>
                    <ErrorBox errorObj={error} />
                </Container>
            )
        },
        element: (
            <QueryParamProvider adapter={ReactRouter6Adapter}>
                <Outlet />
            </QueryParamProvider>
        ),
        children: [
            {
                children: [
                    {
                        element: (
                            <CurrentUserProvider>
                                <Outlet />
                            </CurrentUserProvider>
                        ),
                        ErrorBoundary: () => {
                            const error = useRouteError()
                            return (
                                <Container pt="1rem">
                                    <ErrorBox errorObj={error} />
                                </Container>
                            )
                        },
                        children: [...protectedRoutes],
                    },
                ],
            },

            ...publicRoutes,
        ],
    },
])

import { ErrorBox } from '@/components/error-box'
import { Container, Text, Title } from '@mantine/core'
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
import { ChannelShell } from './features/channel/channel-shell'

const protectedRoutes: RouteObject[] = [
    {
        path: '',
        lazy: () => import('./features/root/root.page'),
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
        ],
    },
]

const publicRoutes: RouteObject[] = [
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
                    <Container pt="1rem">
                        <Title order={1}>{error.status}</Title>
                        <Text>{error.statusText}</Text>
                    </Container>
                )
            }
            return (
                <Container pt="1rem">
                    <ErrorBox errorObj={error} />
                </Container>
            )
        },
        children: [
            {
                path: '',
                children: [
                    {
                        element: (
                            <CurrentUserProvider>
                                <QueryParamProvider
                                    adapter={ReactRouter6Adapter}
                                >
                                    <Outlet />
                                </QueryParamProvider>
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

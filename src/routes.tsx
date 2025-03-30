import { ErrorBox } from '@/components/error-box'
import { Container } from '@mantine/core'
import {
    createBrowserRouter,
    Outlet,
    RouteObject,
    useRouteError,
} from 'react-router-dom'
import { QueryParamProvider } from 'use-query-params'
import { ReactRouter6Adapter } from 'use-query-params/adapters/react-router-6'
import { Shell } from './components/shell'

const protectedRoutes: RouteObject[] = []

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
            return (
                <Container pt="1rem">
                    <ErrorBox errorObj={error} />
                </Container>
            )
        },
        children: [
            {
                path: '/',
                children: [
                    {
                        path: '',
                        element: (
                            <QueryParamProvider adapter={ReactRouter6Adapter}>
                                <Shell>
                                    <Outlet />
                                </Shell>
                            </QueryParamProvider>
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
                    ...publicRoutes,
                ],
            },
        ],
    },
])

import { MantineProvider } from '@mantine/core'
import { ModalsProvider } from '@mantine/modals'
import { Notifications } from '@mantine/notifications'
import { QueryClientProvider } from '@tanstack/react-query'
import React from 'react'
import ReactDOM from 'react-dom/client'
import { RouterProvider } from 'react-router-dom'
import { queryClient } from './queryclient'
import { router } from './routes'
import { theme } from './theme'

import { ContextMenuProvider } from 'mantine-contextmenu'
import './theme.css'

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
    <React.StrictMode>
        <MantineProvider theme={theme} forceColorScheme={'dark'}>
            <ContextMenuProvider>
                <Notifications position="top-right" />
                <QueryClientProvider client={queryClient}>
                    <ModalsProvider>
                        <RouterProvider router={router} />
                    </ModalsProvider>
                </QueryClientProvider>
            </ContextMenuProvider>
        </MantineProvider>
    </React.StrictMode>
)

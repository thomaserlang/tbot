import { Center, Container } from '@mantine/core'
import { AxiosError } from 'axios'
import { createContext, useContext } from 'react'
import { Navigate } from 'react-router-dom'
import { ErrorBox } from '../error-box'
import { Logo } from '../logo'
import { useGetCurrentUser } from './api/current-user.api'
import { CurrentUser } from './current-user.type'

const CurrentUserContext = createContext<CurrentUser | undefined>(undefined)

export function CurrentUserProvider({
    children,
}: {
    children: React.ReactNode
}) {
    const { data, error } = useGetCurrentUser()

    if (!data && error) {
        if (error instanceof AxiosError) {
            if (error?.response?.status == 401)
                return <Navigate to="/sign-in" />
        }
        return (
            <Container mt="2rem">
                <Center mb="2rem">
                    <Logo />
                </Center>
                <ErrorBox errorObj={error} />
            </Container>
        )
    }

    return (
        <CurrentUserContext.Provider value={data}>
            {data && children}
        </CurrentUserContext.Provider>
    )
}

export function useCurrentUser() {
    const currentUserContext = useContext(CurrentUserContext)

    if (!currentUserContext) {
        throw new Error(
            'useCurrentUser has to be used within <CurrentUserProvider>'
        )
    }

    return currentUserContext
}

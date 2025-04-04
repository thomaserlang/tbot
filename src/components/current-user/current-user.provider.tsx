import { Container } from '@mantine/core'
import { createContext, useContext } from 'react'
import { ErrorBox } from '../error-box'
import { useGetCurrentUser } from './current-user.api'
import { ICurrentUser } from './current-user.type'

const CurrentUserContext = createContext<ICurrentUser | undefined>(undefined)

export function CurrentUserProvider({
    children,
}: {
    children: React.ReactNode
}) {
    const { data, error } = useGetCurrentUser()

    if (error)
        return (
            <Container>
                <ErrorBox errorObj={error} />
            </Container>
        )

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

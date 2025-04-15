import { Center, Container } from '@mantine/core'
import { createContext, useContext } from 'react'
import { ErrorBox } from '../error-box'
import { Logo } from '../logo'
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
            <Container mt="2rem">
                <Center mb="2rem">
                    <Logo width="35rem" />
                </Center>
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

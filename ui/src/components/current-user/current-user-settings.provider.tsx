import { UserSettings } from '@/features/user/types/user-settings.type'
import { Center, Container } from '@mantine/core'
import { createContext, useContext } from 'react'
import { ErrorBox } from '../error-box'
import { Logo } from '../logo'
import {
    useGetUserSettings,
    useUpdateUserSettings,
} from './api/current-user-settings.api'

interface UserSettingsProvider {
    settings: UserSettings
    updateSettings: (settings: Partial<UserSettings>) => void
}

const CurrentUserSettingsContext = createContext<
    UserSettingsProvider | undefined
>(undefined)

export function CurrentUserSettingsProvider({
    children,
}: {
    children: React.ReactNode
}) {
    const { data, error } = useGetUserSettings()
    const update = useUpdateUserSettings()

    if (!data && error) {
        return (
            <Container mt="2rem">
                <Center mb="2rem">
                    <Logo />
                </Center>
                <ErrorBox errorObj={error} />
            </Container>
        )
    }

    if (!data) return

    return (
        <CurrentUserSettingsContext.Provider
            value={{
                settings: data,
                updateSettings: (settings: Partial<UserSettings>) => {
                    update.mutate({ settings })
                },
            }}
        >
            {data && children}
        </CurrentUserSettingsContext.Provider>
    )
}

export function useCurrentUserSettings() {
    const context = useContext(CurrentUserSettingsContext)

    if (!context) {
        throw new Error(
            'useCurrentUserSettings has to be used within <CurrentUserSettingsProvider>'
        )
    }

    return context
}

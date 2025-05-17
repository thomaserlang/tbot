import { setAccessToken } from '@/utils/api'
import { Avatar, Flex, Menu } from '@mantine/core'
import { openModal } from '@mantine/modals'
import { IconLogout, IconSettings } from '@tabler/icons-react'
import { useCurrentUser } from './current-user.provider'
import { UserSettingsView } from './settings/user-settings-view'

export function CurrentUserCard() {
    const user = useCurrentUser()
    return (
        <Menu width={200}>
            <Menu.Target>
                <Flex
                    align="center"
                    gap="0.5rem"
                    style={{
                        cursor: 'pointer',
                        userSelect: 'none',
                    }}
                >
                    <Avatar color="blue" size="md" name={user.display_name} />
                </Flex>
            </Menu.Target>
            <Menu.Dropdown>
                <Menu.Item
                    leftSection={<IconLogout size={14} />}
                    onClick={() => {
                        setAccessToken('')
                        location.href = '/sign-in'
                    }}
                >
                    Sign out
                </Menu.Item>
                <Menu.Item
                    leftSection={<IconSettings size={14} />}
                    onClick={() => {
                        openModal({
                            title: 'Settings',
                            children: <UserSettingsView />,
                            size: 'lg',
                            zIndex: 200,
                        })
                    }}
                >
                    Settings
                </Menu.Item>
            </Menu.Dropdown>
        </Menu>
    )
}

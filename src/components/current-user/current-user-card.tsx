import { setAccessToken } from '@/utils/api'
import { Avatar, Flex, Menu, Text } from '@mantine/core'
import { IconChevronDown, IconLogout } from '@tabler/icons-react'
import { useCurrentUser } from './current-user.provider'

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
                    <Avatar color="blue" size="sm" name={user.display_name} />
                    <Text truncate="end" maw={160} size="sm">
                        {user.display_name}
                    </Text>
                    <IconChevronDown size={14} />
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
            </Menu.Dropdown>
        </Menu>
    )
}

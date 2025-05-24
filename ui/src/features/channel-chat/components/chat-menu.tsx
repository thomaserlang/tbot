import { EmulateEventMenuItems } from '@/features/channel-emulate-event'
import { Menu } from '@mantine/core'

interface Props {
    children: React.ReactNode
}

export function ChatMenu({ children }: Props) {
    return (
        <Menu width={200}>
            <Menu.Target>{children}</Menu.Target>

            <Menu.Dropdown>
                <Menu.Sub>
                    <Menu.Sub.Target>
                        <Menu.Sub.Item>Emulate event</Menu.Sub.Item>
                    </Menu.Sub.Target>

                    <Menu.Sub.Dropdown>
                        <EmulateEventMenuItems />
                    </Menu.Sub.Dropdown>
                </Menu.Sub>
            </Menu.Dropdown>
        </Menu>
    )
}

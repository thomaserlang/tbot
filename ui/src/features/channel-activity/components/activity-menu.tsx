import { Menu } from '@mantine/core'
import { IconSettings } from '@tabler/icons-react'
import { useState } from 'react'
import { ActivitySettingsModal } from './activity-settings-modal'

interface Props {
    children: React.ReactElement
}

export function ActivityMenu({ children }: Props) {
    const [openSettings, setOpenSettings] = useState(false)

    return (
        <>
            <Menu width={200}>
                <Menu.Target>{children}</Menu.Target>

                <Menu.Dropdown>
                    <Menu.Item
                        leftSection={<IconSettings size={16} />}
                        onClick={() => setOpenSettings(true)}
                    >
                        Settings
                    </Menu.Item>
                </Menu.Dropdown>
            </Menu>

            {openSettings && (
                <ActivitySettingsModal
                    opened={openSettings}
                    onClose={() => setOpenSettings(false)}
                />
            )}
        </>
    )
}

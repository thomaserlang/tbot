import { useDisclosure } from '@mantine/hooks'
import { cloneElement } from 'react'
import { ActivitySettingsModal } from './activity-settings-modal'

interface Props {
    children: React.ReactElement<{
        onClick: () => void
    }>
}

export function ActivitySettings({ children }: Props) {
    const [opened, { open, close }] = useDisclosure(false)
    return (
        <>
            {cloneElement(children, {
                onClick: open,
            })}

            <ActivitySettingsModal opened={opened} onClose={close} />
        </>
    )
}

import { Modal } from '@mantine/core'
import { ActivitySettingsForm } from './activity-settings-form'

interface Props {
    opened: boolean
    onClose: () => void
}

export function ActivitySettingsModal({ opened, onClose }: Props) {
    return (
        <Modal title="Activity Feed Settings" opened={opened} onClose={onClose}>
            {opened && <ActivitySettingsForm />}
        </Modal>
    )
}

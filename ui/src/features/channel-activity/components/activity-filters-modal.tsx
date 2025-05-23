import { Modal } from '@mantine/core'
import { ActivityFiltersForm } from './activity-filters-form'

interface Props {
    opened: boolean
    onClose: () => void
}

export function ActivityFiltersModal({ opened, onClose }: Props) {
    return (
        <Modal
            opened={opened}
            onClose={onClose}
            title="Activity Feed Filters"
            size="lg"
        >
            {opened && <ActivityFiltersForm />}
        </Modal>
    )
}

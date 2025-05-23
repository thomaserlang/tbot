import { useDisclosure } from '@mantine/hooks'
import React from 'react'
import { ActivityFiltersModal } from './activity-filters-modal'

interface Props {
    children: React.ReactElement<{
        onClick: () => void
    }>
}

export function ActivityFilters({ children }: Props) {
    const [opened, { open, close }] = useDisclosure(false)

    return (
        <>
            {React.cloneElement(children, {
                onClick: () => {
                    open()
                    children.props.onClick?.()
                },
            })}

            <ActivityFiltersModal opened={opened} onClose={close} />
        </>
    )
}

import { useDisclosure } from '@mantine/hooks'
import React, { cloneElement } from 'react'
import { CommandTemplate } from '../types/command-template.types'
import { CommandTemplateSelectModal } from './command-template-select-modal'

interface Props {
    children: React.ReactElement<{
        onClick: () => void
    }>
    onSelect: (commandTemplate: CommandTemplate) => void
}

export function CommandTemplateSelect({ children, onSelect }: Props) {
    const [opened, { open, close }] = useDisclosure(false)

    return (
        <>
            {cloneElement(children, {
                onClick: () => {
                    children.props.onClick?.()
                    open()
                },
            })}

            <CommandTemplateSelectModal
                opened={opened}
                onClose={close}
                onSelect={(commandTemplate) => {
                    onSelect?.(commandTemplate)
                    close()
                }}
            />
        </>
    )
}

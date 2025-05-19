import { ChannelId } from '@/features/channel/types/channel.types'
import { useDisclosure } from '@mantine/hooks'
import React from 'react'
import { Command } from '../types/command.types'
import { CommandCreateModal } from './command-create-modal'

interface Props {
    children: React.ReactElement<{
        loading: boolean
        onClick: () => void
    }>
    channelId: ChannelId
    onCreated?: (command: Command) => void
}

export function CommandCreate({ channelId, children, onCreated }: Props) {
    const [opened, { open, close }] = useDisclosure(false)
    return (
        <>
            {React.cloneElement(children, {
                onClick: () => {
                    children.props.onClick?.()
                    open()
                },
            })}

            <CommandCreateModal
                channelId={channelId}
                opened={opened}
                onClose={close}
                onCreated={onCreated}
            />
        </>
    )
}

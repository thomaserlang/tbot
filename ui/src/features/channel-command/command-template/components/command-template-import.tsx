import { useCurrentChannel } from '@/features/channel/current-channel.provider'
import { toastPromise } from '@/utils/toast'
import { useState } from 'react'
import { createCommand } from '../../command/api/command.api'
import { CommandTemplate } from '../types/command-template.types'
import { CommandTemplateCommandsSelectModal } from './command-template-commands-select-modal'
import { CommandTemplateSelect } from './command-template-select'

interface Props {
    children: React.ReactElement<{
        loading: boolean
        onClick: () => void
    }>
}

export function CommandTemplateImport({ children }: Props) {
    const [commandTemplate, setCommandTemplate] =
        useState<CommandTemplate | null>(null)
    const channel = useCurrentChannel()

    return (
        <>
            <CommandTemplateSelect
                onSelect={(commandTemplate) => {
                    setCommandTemplate(commandTemplate)
                }}
            >
                {children}
            </CommandTemplateSelect>

            {commandTemplate && (
                <CommandTemplateCommandsSelectModal
                    opened={!!commandTemplate}
                    commandTemplate={commandTemplate}
                    onClose={() => setCommandTemplate(null)}
                    onSelect={(commands) => {
                        for (const command of commands) {
                            toastPromise({
                                promise: createCommand({
                                    channelId: channel.id,
                                    data: command,
                                }),
                                loading: {
                                    title: `Creating ${command.cmds
                                        ?.map((cmd) => `!${cmd}`)
                                        .join(', ')}}`,
                                },
                                success: {
                                    title: `${command.cmds
                                        ?.map((cmd) => `!${cmd}`)
                                        .join(', ')}} created`,
                                },
                                error: {
                                    title: `Failed to create ${command.cmds
                                        ?.map((cmd) => `!${cmd}`)
                                        .join(', ')}}`,
                                },
                            })
                        }
                    }}
                />
            )}
        </>
    )
}

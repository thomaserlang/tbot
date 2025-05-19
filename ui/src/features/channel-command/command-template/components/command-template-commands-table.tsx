import { ActionIcon, Anchor } from '@mantine/core'
import { IconTrash } from '@tabler/icons-react'
import { DataTable } from 'mantine-datatable'
import { CommandCreate } from '../../command/types/command.types'

interface Props {
    commands: CommandCreate[]
    onDelete?: (index: number) => void
    onEdit?: (index: number) => void
    selectedCommands?: CommandCreate[]
    onSelect?: (commands: CommandCreate[]) => void
}

export function CommandTemplateCommandsTable({
    commands,
    selectedCommands,
    onSelect,
    onDelete,
    onEdit,
}: Props) {
    return (
        <DataTable
            idAccessor={(row) => `${commands.indexOf(row)}`}
            highlightOnHover
            records={commands}
            minHeight={150}
            noRecordsText="No commands"
            withTableBorder
            onSelectedRecordsChange={(commands) => onSelect?.(commands)}
            selectedRecords={selectedCommands}
            columns={[
                {
                    accessor: 'cmds',
                    title: 'Command/Pattern',
                    width: '25%',
                    render: (row, index) => {
                        if (!onEdit)
                            return (
                                <span>
                                    {row.cmds
                                        ?.map((cmd) => `!${cmd}`)
                                        .join(', ')}
                                    {!row.cmds && row.patterns?.join(', ')}
                                </span>
                            )

                        return (
                            <Anchor size="sm" onClick={() => onEdit?.(index)}>
                                {row.cmds?.map((cmd) => `!${cmd}`).join(', ')}
                                {!row.cmds && row.patterns?.join(', ')}
                            </Anchor>
                        )
                    },
                },
                {
                    accessor: 'response',
                    title: 'Response',
                },
                {
                    accessor: '',
                    width: '1%',
                    hidden: !onDelete,
                    render: (_, index) => (
                        <ActionIcon
                            onClick={() => onDelete?.(index)}
                            variant="subtle"
                            color="red"
                            size="sm"
                        >
                            <IconTrash size={18} />
                        </ActionIcon>
                    ),
                },
            ]}
        />
    )
}

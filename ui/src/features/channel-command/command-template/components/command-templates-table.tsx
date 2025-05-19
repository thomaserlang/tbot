import { ErrorBox } from '@/components/error-box'
import { pageRecordsFlatten } from '@/utils/page-records'
import { Anchor } from '@mantine/core'
import { IconBlocks } from '@tabler/icons-react'
import { DataTable } from 'mantine-datatable'
import { useGetCommandTemplates } from '../api/command-templates.api'
import { CommandTemplate } from '../types/command-template.types'
import { CommandTemplateMenu } from './command-template-menu'

interface Props {
    onEditClick?: (command: CommandTemplate) => void
}

export function CommandTemplatesTable({ onEditClick }: Props) {
    const data = useGetCommandTemplates()

    if (data.error) return <ErrorBox errorObj={data.error} />

    return (
        <DataTable
            records={pageRecordsFlatten(data.data)}
            withTableBorder
            highlightOnHover
            onScrollToBottom={() => data.fetchNextPage()}
            fetching={data.isLoading}
            h="100%"
            fz="md"
            noRecordsText="No command templates, create one."
            noRecordsIcon={<IconBlocks size={80} />}
            columns={[
                {
                    accessor: 'title',
                    title: 'Name',
                    width: '25%',

                    render: (row) => (
                        <Anchor onClick={() => onEditClick?.(row)}>
                            {row.title}
                        </Anchor>
                    ),
                },
                {
                    accessor: '',
                    width: '1%',
                    noWrap: true,
                    textAlign: 'right',
                    render: (row) => (
                        <CommandTemplateMenu
                            commandTemplate={row}
                            onEditClick={onEditClick}
                        />
                    ),
                },
            ]}
        />
    )
}

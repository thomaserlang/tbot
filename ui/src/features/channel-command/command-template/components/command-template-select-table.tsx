import { ErrorBox } from '@/components/error-box'
import { NestedSelect } from '@/components/nested-select'
import { pageRecordsFlatten } from '@/utils/page-records'
import { useEffect } from 'react'
import { useGetCommandTemplates } from '../api/command-templates.api'
import { CommandTemplate } from '../types/command-template.types'

interface Props {
    onSelect: (commandTemplate: CommandTemplate) => void
}

export function CommandTemplateSelectTable({ onSelect }: Props) {
    const { data, isLoading, isFetchingNextPage, fetchNextPage, error } =
        useGetCommandTemplates()

    useEffect(() => {
        fetchNextPage()
    }, [data])

    if (error) return <ErrorBox errorObj={error} />

    return (
        <NestedSelect
            noRecordsText="No command templates"
            isLoading={isLoading || isFetchingNextPage}
            onSelect={onSelect}
            data={pageRecordsFlatten(data).map((d) => ({
                value: d.id,
                name: d.title,
                object: d,
            }))}
        />
    )
}

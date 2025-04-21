import { ErrorBox } from '@/components/error-box'
import { PageLoader } from '@/components/page-loader'
import { providerInfo } from '@/constants'
import { Flex, Input, Text } from '@mantine/core'
import { IconSearch } from '@tabler/icons-react'
import { DataTable } from 'mantine-datatable'
import { useState } from 'react'
import { useGetViewerSearch } from '../api/viewer-search'
import { ViewerName } from '../types/viewer.type'

interface Props {
    onSelect?: (viewer: ViewerName) => void
}

export function ViewerSearch({ onSelect }: Props) {
    const [name, setName] = useState<string>('')
    const { data, isLoading, error } = useGetViewerSearch({
        query: name,
    })
    return (
        <Flex gap="1rem" direction="column">
            <Input
                placeholder="Search..."
                w="100%"
                rightSection={<IconSearch />}
                data-autofocus
                onChange={(e) => {
                    setName(e.currentTarget.value)
                }}
            />

            {isLoading && <PageLoader />}

            {error && <ErrorBox errorObj={error} />}

            {data && (
                <DataTable
                    records={data}
                    maxHeight={400}
                    fz="xl"
                    noHeader
                    withTableBorder
                    borderRadius="xs"
                    highlightOnHover
                    fetching={isLoading}
                    minHeight={200}
                    noRecordsText="No viewers found"
                    onRowClick={({ record }) => {
                        onSelect?.(record)
                    }}
                    columns={[
                        {
                            accessor: 'display_name',
                        },
                        {
                            accessor: 'provider',
                            width: '1%',
                            noWrap: true,
                            render: (row) => (
                                <Text c="dimmed" fz="xl">
                                    {providerInfo[row.provider].name ||
                                        row.provider}
                                </Text>
                            ),
                        },
                    ]}
                />
            )}
        </Flex>
    )
}

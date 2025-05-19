import { IListToGroupsItem } from '@/utils/group-data'
import { Autocomplete } from '@mantine/core'
import { IconSearch } from '@tabler/icons-react'
import Fuse from 'fuse.js'
import { useMemo } from 'react'

interface IProps<T> {
    data: IListToGroupsItem<T>[]
    onResults: (results: IListToGroupsItem<T>[]) => void
}

export function SelectNestedSearch<T>({ data, onResults }: IProps<T>) {
    const fuse = useMemo(() => {
        return new Fuse(data, {
            keys: ['name', 'group'],
            shouldSort: false,
            threshold: 0.1,
            ignoreLocation: true,
        })
    }, [data])

    return (
        <Autocomplete
            leftSection={<IconSearch size="14" />}
            placeholder="Søg..."
            clearable
            data-autofocus
            onChange={(value) => {
                if (value === '') {
                    onResults(data)
                    return
                }
                const results = fuse.search(value)
                onResults(results.map((r) => r.item))
            }}
        />
    )
}

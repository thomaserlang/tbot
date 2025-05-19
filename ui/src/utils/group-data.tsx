import { splitGroup } from './split'

export interface IListToGroupsItem<T = undefined> {
    value: string
    name: string
    group?: string
    object: T
}

export interface IListGroupedItem<T = undefined> {
    value: string
    name: string
    object: T | null
    items: IListGroupedItem<T>[] | null
}

export function listToGroups<T = undefined>(
    items: IListToGroupsItem<T>[]
): IListGroupedItem<T>[] {
    const grouped: { [key: string]: IListGroupedItem<T>[] } = {
        '': [],
    }

    for (const item of items) {
        let nested = ''
        for (const s of splitGroup(item.group || '')) {
            const before = nested
            nested += `${s.toLowerCase()}.`
            if (!(nested in grouped)) {
                grouped[nested] = []
                grouped[before].push({
                    value: nested,
                    name: s,
                    object: null,
                    items: grouped[nested],
                })
            }
        }
        grouped[nested].push({
            value: item.value,
            name: item.name,
            object: item.object,
            items: null,
        })
    }
    return grouped['']
}

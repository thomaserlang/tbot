import { PageCursor } from '@/types/page-cursor.type'
import { InfiniteData } from '@tanstack/react-query'

export function mergePageLookupData<
    T = Record<string, unknown>,
    L = Record<string, unknown[]>
>(data: InfiniteData<PageCursor<T, L>>): L {
    if (!data) return {} as L
    const lookupData = data.pages[0].lookup_data
    for (const page of data.pages)
        for (const key in page.lookup_data)
            lookupData[key] = { ...lookupData[key], ...page.lookup_data[key] }
    return lookupData
}

export function pageRecordsFlatten<T = Record<string, unknown>, L = unknown>(
    data: InfiniteData<PageCursor<T, L>> | undefined
): T[] {
    if (!data) return []
    return data.pages.map((p) => p.records).flat()
}

export function removeRecord<T>(
    oldData: InfiniteData<PageCursor<T>> | undefined,
    matchFn: (item: T) => boolean
): InfiniteData<PageCursor<T>> | undefined {
    if (!oldData) return oldData
    const pages = oldData.pages.map((page) => ({
        ...page,
        records: page.records.filter((item) => matchFn(item)),
    }))
    return {
        ...oldData,
        pages,
    }
}

export function updateRecord<T>(
    oldData: InfiniteData<PageCursor<T>> | undefined,
    updatedRecord: T,
    matchFn: (item: T) => boolean
): InfiniteData<PageCursor<T>> | undefined {
    if (!oldData) return oldData
    const pages = oldData.pages.map((page) => ({
        ...page,
        records: page.records.map((item) =>
            matchFn(item) ? updatedRecord : item
        ),
    }))
    return {
        ...oldData,
        pages,
    }
}

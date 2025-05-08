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

export function addRecord<T = Record<string, unknown>, L = any>({
    oldData,
    data,
    maxSize,
}: {
    oldData: InfiniteData<PageCursor<T, L>> | undefined
    data: T
    maxSize?: number
}): InfiniteData<PageCursor<T, L>> | undefined {
    if (!oldData) return oldData
    const pages = oldData.pages.map((page, index) => ({
        ...page,
        records:
            index === 0
                ? maxSize
                    ? [data, ...page.records.slice(0, maxSize - 1)]
                    : [data, ...page.records]
                : page.records,
    }))
    return {
        ...oldData,
        pages,
    }
}

export function updateRecord<T = Record<string, unknown>, L = any>({
    oldData,
    data,
    matchFn,
}: {
    oldData: InfiniteData<PageCursor<T, L>> | undefined
    data: T
    matchFn: (item: T) => boolean
}): InfiniteData<PageCursor<T, L>> | undefined {
    if (!oldData) return oldData
    const pages = oldData.pages.map((page) => ({
        ...page,
        records: page.records.map((item) => (matchFn(item) ? data : item)),
    }))
    return {
        ...oldData,
        pages,
    }
}

export function removeRecord<T = Record<string, unknown>, L = any>({
    oldData,
    matchFn,
}: {
    oldData: InfiniteData<PageCursor<T, L>> | undefined
    matchFn: (item: T) => boolean
}): InfiniteData<PageCursor<T, L>> | undefined {
    if (!oldData) return oldData
    const pages = oldData.pages.map((page) => ({
        ...page,
        records: page.records.filter((item) => !matchFn(item)),
    }))
    return {
        ...oldData,
        pages,
    }
}

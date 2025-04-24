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

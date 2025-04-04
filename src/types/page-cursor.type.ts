export type LookupData<T = any> = {
    [keyName: string]: { [idOfKey: string]: T }
}

export interface PageCursor<T = any, L = LookupData> {
    records: T[]
    total: number
    cursor: string | null
    lookup_data: L
}

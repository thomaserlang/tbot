export type TLookupData<T = any> = {
    [keyName: string]: { [idOfKey: string]: T }
}

export interface IPageCursor<T = any, L = TLookupData> {
    records: T[]
    total: number
    cursor: string | null
    lookup_data: L
}

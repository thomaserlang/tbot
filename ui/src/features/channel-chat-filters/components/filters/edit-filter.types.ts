export interface EditFilterProps<T> {
    filter: T
    onUpdated?: (filter: T) => void
}

import { Provider } from '@/types/provider.type'

export interface ActivityTypeName {
    name: string
    display_name: string
    color: string
    provider: Provider
    count_name: string
    filter_min_count?: boolean
    sub_type_names?: Record<string, string>
}

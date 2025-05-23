import { Branded } from '@/utils/brand'

export type UserId = Branded<string, 'UserId'>

export interface User {
    id: string
    username: string
    display_name: string
    default_channel_id: string
}

import { ChatFilterId } from '@/features/channel-chat-filters/filter.types'
import { Branded } from '@/utils/brand'

export type BannedTermId = Branded<string, 'BannedTermId'>

export type BannedTermType = 'phrase' | 'regex'

export const bannedTermTypeLabels: { [type: string | BannedTermType]: string } =
    {
        phrase: 'Phrase',
        regex: 'Regex',
    }

export interface BannedTerm {
    id: BannedTermId
    chat_filter_id: ChatFilterId
    type: BannedTermType
    text: string
}

export interface BannedTermRequest {
    type: BannedTermType
    text: string
}

import {
    ChatFilterBannedTerms,
    ChatFilterBannedTermsRequest,
    EditBannedTermsFilter,
} from './components/filters/banned-terms/edit-banned-terms-filter'
import {
    ChatFilterCaps,
    ChatFilterCapsRequest,
    EditCapsFilter,
} from './components/filters/edit-caps-filter'
import {
    ChatFilterEmote,
    ChatFilterEmoteRequest,
    EditEmoteFilter,
} from './components/filters/edit-emote-filter'
import {
    ChatFilterLink,
    ChatFilterLinkRequest,
    EditLinkFilter,
} from './components/filters/edit-link-filter'
import {
    ChatFilterNonLatin,
    ChatFilterNonLatinRequest,
    EditNonLatinFilter,
} from './components/filters/edit-non-latin-filter'
import {
    ChatFilterParagraph,
    ChatFilterParagraphRequest,
    EditParagraphFilter,
} from './components/filters/edit-paragraph-filter'
import {
    ChatFilterSymbol,
    ChatFilterSymbolRequest,
    EditSymbolFilter,
} from './components/filters/edit-symbol-filter'

export type ChatFilter =
    | ChatFilterBannedTerms
    | ChatFilterCaps
    | ChatFilterEmote
    | ChatFilterLink
    | ChatFilterNonLatin
    | ChatFilterParagraph
    | ChatFilterSymbol

export type ChatFilterRequest =
    | ChatFilterBannedTermsRequest
    | ChatFilterCapsRequest
    | ChatFilterEmoteRequest
    | ChatFilterLinkRequest
    | ChatFilterNonLatinRequest
    | ChatFilterParagraphRequest
    | ChatFilterSymbolRequest

export const registeredFilters: {
    [P in ChatFilter['type']]: {
        name: string
        type: P
        component: React.FC<{
            filter: Extract<ChatFilter, { type: P }>
        }>
    }
} = {
    caps: {
        name: 'Caps Filter',
        type: 'caps',
        component: EditCapsFilter,
    },
    emote: {
        name: 'Emote Filter',
        type: 'emote',
        component: EditEmoteFilter,
    },
    non_latin: {
        name: 'Non-latin Filter',
        type: 'non_latin',
        component: EditNonLatinFilter,
    },
    paragraph: {
        name: 'Paragraph Filter',
        type: 'paragraph',
        component: EditParagraphFilter,
    },
    symbol: {
        name: 'Symbol Filter',
        type: 'symbol',
        component: EditSymbolFilter,
    },
    banned_terms: {
        name: 'Banned Terms Filter',
        type: 'banned_terms',
        component: EditBannedTermsFilter,
    },
    link: {
        name: 'Link Filter',
        type: 'link',
        component: EditLinkFilter,
    },
} as const

import { NumberInput, SimpleGrid } from '@mantine/core'
import { useForm } from '@mantine/form'
import { filterToBaseRequest } from '../../filter-utils'
import { ChatFilterBase, ChatFilterRequestBase } from '../../filter.types'
import { EditFilterForm } from '../filter-edit-form'
import { EditFilterProps } from './edit-filter.types'

export interface ChatFilterSymbolSettings {
    max_symbols: number
}

export interface ChatFilterSymbolRequest extends ChatFilterRequestBase {
    type: 'symbol'
    settings?: ChatFilterSymbolSettings
}
export interface ChatFilterSymbol extends ChatFilterBase {
    type: 'symbol'
    settings: ChatFilterSymbolSettings
}

export function EditSymbolFilter(props: EditFilterProps<ChatFilterSymbol>) {
    const form = useForm<ChatFilterSymbolRequest>({
        mode: 'uncontrolled',
        initialValues: {
            ...filterToBaseRequest(props.filter),
            type: props.filter.type,
            settings: {
                max_symbols: props.filter.settings.max_symbols,
            },
        },
    })

    return (
        <EditFilterForm<ChatFilterSymbol> {...props} form={form}>
            <SimpleGrid cols={{ base: 2, md: 3 }}>
                <NumberInput
                    label="Max symbols"
                    key={form.key('settings.max_symbols')}
                    allowNegative={false}
                    {...form.getInputProps('settings.max_symbols')}
                />
            </SimpleGrid>
        </EditFilterForm>
    )
}

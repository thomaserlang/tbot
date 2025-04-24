import { NumberInput, SimpleGrid } from '@mantine/core'
import { useForm } from '@mantine/form'
import { filterToBaseRequest } from '../../filter-utils'
import { ChatFilterBase, ChatFilterRequestBase } from '../../filter.types'
import { EditFilterForm } from '../filter-edit-form'
import { EditFilterProps } from './edit-filter.types'

export interface ChatFilterNonLatinSettings {
    min_length: number
    max_percent: number
}

export interface ChatFilterNonLatinRequest extends ChatFilterRequestBase {
    type: 'non_latin'
    settings?: ChatFilterNonLatinSettings
}
export interface ChatFilterNonLatin extends ChatFilterBase {
    type: 'non_latin'
    settings: ChatFilterNonLatinSettings
}

export function EditNonLatinFilter(props: EditFilterProps<ChatFilterNonLatin>) {
    const form = useForm<ChatFilterNonLatinRequest>({
        mode: 'uncontrolled',
        initialValues: {
            ...filterToBaseRequest(props.filter),
            type: props.filter.type,
            settings: {
                min_length: props.filter.settings.min_length,
                max_percent: props.filter.settings.max_percent,
            },
        },
    })

    return (
        <EditFilterForm {...props} form={form}>
            <SimpleGrid cols={{ base: 2, md: 3 }}>
                <NumberInput
                    label="Min length"
                    key={form.key('settings.min_length')}
                    allowNegative={false}
                    {...form.getInputProps('settings.min_length')}
                />
                <NumberInput
                    label="Max percentage"
                    key={form.key('settings.max_percent')}
                    allowNegative={false}
                    {...form.getInputProps('settings.max_percent')}
                />
            </SimpleGrid>
        </EditFilterForm>
    )
}

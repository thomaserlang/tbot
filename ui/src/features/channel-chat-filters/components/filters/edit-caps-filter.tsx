import { SimpleGrid, TextInput } from '@mantine/core'
import { useForm } from '@mantine/form'
import { filterToBaseRequest } from '../../filter-utils'
import { ChatFilterBase, ChatFilterRequestBase } from '../../filter.types'
import { EditFilterForm } from '../filter-edit-form'
import { EditFilterProps } from './edit-filter.types'

export interface ChatFilterCapsSettings {
    min_length: number
    max_percent: number
}

export interface ChatFilterCapsRequest extends ChatFilterRequestBase {
    type: 'caps'
    settings?: ChatFilterCapsSettings
}
export interface ChatFilterCaps extends ChatFilterBase {
    type: 'caps'
    settings: ChatFilterCapsSettings
}

export function EditCapsFilter(props: EditFilterProps<ChatFilterCaps>) {
    const form = useForm<ChatFilterCapsRequest>({
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
                <TextInput
                    label="Minimum length"
                    key={form.key('settings.min_length')}
                    {...form.getInputProps('settings.min_length')}
                />

                <TextInput
                    label="Maximum percent"
                    key={form.key('settings.max_percent')}
                    {...form.getInputProps('settings.max_percent')}
                />
            </SimpleGrid>
        </EditFilterForm>
    )
}

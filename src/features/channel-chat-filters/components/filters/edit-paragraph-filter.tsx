import { NumberInput, SimpleGrid } from '@mantine/core'
import { useForm } from '@mantine/form'
import { filterToBaseRequest } from '../../filter-utils'
import { ChatFilterBase, ChatFilterRequestBase } from '../../filter.types'
import { EditFilterForm } from '../filter-edit-form'
import { EditFilterProps } from './edit-filter.types'

export interface ChatFilterParagraphSettings {
    max_length: number
}

export interface ChatFilterParagraphRequest extends ChatFilterRequestBase {
    type: 'paragraph'
    settings?: ChatFilterParagraphSettings
}

export interface ChatFilterParagraph extends ChatFilterBase {
    type: 'paragraph'
    settings: ChatFilterParagraphSettings
}

export function EditParagraphFilter(
    props: EditFilterProps<ChatFilterParagraph>
) {
    const form = useForm<ChatFilterParagraphRequest>({
        mode: 'uncontrolled',
        initialValues: {
            ...filterToBaseRequest(props.filter),
            type: props.filter.type,
            settings: {
                max_length: props.filter.settings.max_length,
            },
        },
    })

    return (
        <EditFilterForm<ChatFilterParagraph> {...props} form={form}>
            <SimpleGrid cols={{ base: 2, md: 3 }}>
                <NumberInput
                    label="Max length"
                    key={form.key('settings.max_length')}
                    allowNegative={false}
                    {...form.getInputProps('settings.max_length')}
                />
            </SimpleGrid>
        </EditFilterForm>
    )
}

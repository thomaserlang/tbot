import { NumberInput, SimpleGrid } from '@mantine/core'
import { useForm } from '@mantine/form'
import { filterToBaseRequest } from '../../filter-utils'
import { ChatFilterBase, ChatFilterRequestBase } from '../../filter.types'
import { EditFilterForm } from '../filter-edit-form'
import { EditFilterProps } from './edit-filter.types'

export interface ChatFilterEmoteSettings {
    max_emotes: number
}

export interface ChatFilterEmoteRequest extends ChatFilterRequestBase {
    type: 'emote'
    settings?: ChatFilterEmoteSettings
}
export interface ChatFilterEmote extends ChatFilterBase {
    type: 'emote'
    settings: ChatFilterEmoteSettings
}

export function EditEmoteFilter(props: EditFilterProps<ChatFilterEmote>) {
    const form = useForm<ChatFilterEmoteRequest>({
        mode: 'uncontrolled',
        initialValues: {
            ...filterToBaseRequest(props.filter),
            type: props.filter.type,
            settings: {
                max_emotes: props.filter.settings.max_emotes,
            },
        },
    })

    return (
        <EditFilterForm {...props} form={form}>
            <SimpleGrid cols={{ base: 2, md: 3 }}>
                <NumberInput
                    label="Max emotes"
                    key={form.key('settings.max_emotes')}
                    allowNegative={false}
                    {...form.getInputProps('settings.max_emotes')}
                />
            </SimpleGrid>
        </EditFilterForm>
    )
}

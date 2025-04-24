import { useForm } from '@mantine/form'
import { filterToBaseRequest } from '../../filter-utils'
import { ChatFilterBase, ChatFilterRequestBase } from '../../filter.types'
import { EditFilterForm } from '../filter-edit-form'
import { EditFilterProps } from './edit-filter.types'

export interface ChatFilterLinkRequest extends ChatFilterRequestBase {
    type: 'link'
}
export interface ChatFilterLink extends ChatFilterBase {
    type: 'link'
}

export function EditLinkFilter(props: EditFilterProps<ChatFilterLink>) {
    const form = useForm<ChatFilterLinkRequest>({
        mode: 'uncontrolled',
        initialValues: {
            ...filterToBaseRequest(props.filter),
            type: props.filter.type,
        },
    })

    return <EditFilterForm {...props} form={form}></EditFilterForm>
}

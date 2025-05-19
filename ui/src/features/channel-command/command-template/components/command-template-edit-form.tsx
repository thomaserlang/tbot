import { setFormErrors } from '@/utils/form'
import { toastError, toastSuccess } from '@/utils/toast'
import { Button, Flex } from '@mantine/core'
import { useForm } from '@mantine/form'
import { useUpdateCommandTemplate } from '../api/command-template.api'
import {
    CommandTemplate,
    CommandTemplateUpdate,
} from '../types/command-template.types'
import { CommandTemplateForm } from './command-template-form'

interface Props {
    commandTemplate: CommandTemplate
    onUpdated?: (template: CommandTemplate) => void
}

export function CommandTemplateEditForm({ commandTemplate, onUpdated }: Props) {
    const form = useForm<CommandTemplateUpdate>({
        mode: 'uncontrolled',
        initialValues: {
            title: commandTemplate.title,
            commands: commandTemplate.commands,
        },
    })
    const update = useUpdateCommandTemplate({
        onSuccess: (template) => {
            toastSuccess('Command template saved')
            onUpdated?.(template)
        },
        onError: (error) => {
            if (error.status === 422) setFormErrors(form, error.response.data)
            toastError(error)
        },
    })

    return (
        <form
            onSubmit={form.onSubmit((values) => {
                update.mutate({
                    commandTemplateId: commandTemplate.id,
                    data: values,
                })
            })}
        >
            <CommandTemplateForm form={form} />

            <Flex justify="flex-end" mt="1rem">
                <Button loading={update.isPending} type="submit">
                    Save
                </Button>
            </Flex>
        </form>
    )
}

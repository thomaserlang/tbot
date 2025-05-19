import { setFormErrors } from '@/utils/form'
import { toastError, toastSuccess } from '@/utils/toast'
import { Button, Flex } from '@mantine/core'
import { useForm } from '@mantine/form'
import { useCreateCommandTemplate } from '../api/command-template.api'
import {
    CommandTemplate,
    CommandTemplateCreate,
} from '../types/command-template.types'
import { CommandTemplateForm } from './command-template-form'

interface Props {
    initialValues?: CommandTemplateCreate
    onCreated?: (template: CommandTemplate) => void
}

export function CommandTemplateCreateForm({ initialValues, onCreated }: Props) {
    const form = useForm<CommandTemplateCreate>({
        mode: 'uncontrolled',
        initialValues: {
            title: '',
            commands: [],
            ...initialValues,
        },
    })
    const create = useCreateCommandTemplate({
        onSuccess: (template) => {
            toastSuccess('Command template created')
            onCreated?.(template)
        },
        onError: (error) => {
            if (error.status === 422) setFormErrors(form, error.response.data)
            toastError(error)
        },
    })

    return (
        <form
            onSubmit={form.onSubmit((values) => {
                create.mutate({
                    data: values,
                })
            })}
        >
            <CommandTemplateForm form={form} />

            <Flex justify="flex-end" mt="1rem">
                <Button loading={create.isPending} type="submit">
                    Create
                </Button>
            </Flex>
        </form>
    )
}

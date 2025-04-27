import { UseFormReturnType } from '@mantine/form'

export function set_form_errors(form: UseFormReturnType<any>, error: APIError) {
    for (const e of error.errors) {
        form.setFieldError(e.field, e.message)
    }
}

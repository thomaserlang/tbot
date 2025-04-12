import { Alert, Button, Flex } from '@mantine/core'
import { UseFormReturnType } from '@mantine/form'
import { AxiosError } from 'axios'
import { ChatFilter } from '../filter-registry'
import { useUpdateChatFilter } from '../filter.api'
import { ChatFilterRequestBase } from '../filter.types'
import { FilterForm } from './filter-base-form'

interface Props<F> {
    filter: F
    form: UseFormReturnType<ChatFilterRequestBase>
    children?: React.ReactNode
    onUpdated?: (filter: F) => void
}

export function EditFilterForm<F extends ChatFilter>({
    filter,
    form,
    children,
    onUpdated,
}: Props<F>) {
    const update = useUpdateChatFilter({
        onSuccess: (data) => {
            onUpdated?.(data as F)
        },
        onError: (error) => {
            if (error instanceof AxiosError) {
                if (error.status === 422) {
                    for (const e of error.response?.data.detail) {
                        form.setFieldError(
                            e.loc[1],
                            e.msg.replace('String', '')
                        )
                    }
                }
            }
        },
    })

    return (
        <form
            onSubmit={form.onSubmit((values) => {
                update.mutate({
                    channelId: filter.channel_id,
                    filterId: filter.id,
                    data: values,
                })
            })}
        >
            <Flex gap="1rem" direction="column">
                {children}

                <FilterForm form={form} />

                {update.isError && (
                    <Alert color="red" title="Failed to update the command" />
                )}

                <Flex>
                    <Button ml="auto" type="submit" loading={update.isPending}>
                        Save
                    </Button>
                </Flex>
            </Flex>
        </form>
    )
}

import { setFormErrors } from '@/utils/form'
import { toastError } from '@/utils/toast'
import { Button, Flex } from '@mantine/core'
import { useForm } from '@mantine/form'
import { useUpdateQuote } from '../api/quote.api'
import { ChannelQuote, ChannelQuoteUpdate } from '../types/quote.types'
import { QuoteForm } from './quote-form'

interface Props {
    quote: ChannelQuote
    onUpdated?: (quote: ChannelQuote) => void
}

export function EditQuoteForm({ quote, onUpdated }: Props) {
    const update = useUpdateQuote({
        onSuccess: (data) => {
            onUpdated?.(data)
        },
        onError: (error) => {
            if (error.status === 422) setFormErrors(form, error.response.data)
            else toastError(error)
        },
    })

    const form = useForm<ChannelQuoteUpdate>({
        initialValues: {
            message: quote.message,
            provider: quote.provider,
            created_by_provider_viewer_id: quote.created_by_provider_viewer_id,
            created_by_display_name: quote.created_by_display_name,
        },
    })

    return (
        <form
            onSubmit={form.onSubmit((values) => {
                update.mutate({
                    channelId: quote.channel_id,
                    channelQuoteId: quote.id,
                    data: values,
                })
            })}
        >
            <Flex direction={'column'} gap="1rem">
                <QuoteForm form={form} />

                <Flex>
                    <Button loading={update.isPending} ml="auto" type="submit">
                        Save
                    </Button>
                </Flex>
            </Flex>
        </form>
    )
}

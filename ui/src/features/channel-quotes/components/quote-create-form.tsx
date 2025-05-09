import { ChannelId } from '@/features/channel/types/channel.types'
import { setFormErrors } from '@/utils/form'
import { toastError } from '@/utils/toast'
import { Button, Flex } from '@mantine/core'
import { useForm } from '@mantine/form'
import { useCreateQuote } from '../api/quote.api'
import { ChannelQuote, ChannelQuoteCreate } from '../types/quote.types'
import { QuoteForm } from './quote-form'

interface Props {
    channelId: ChannelId
    onCreated?: (quote: ChannelQuote) => void
}

export function QuoteCreateForm({ channelId, onCreated }: Props) {
    const create = useCreateQuote({
        onSuccess: (data) => {
            onCreated?.(data)
        },
        onError: (error) => {
            if (error.status === 422) setFormErrors(form, error.response.data)
            else toastError(error)
        },
    })
    const form = useForm<ChannelQuoteCreate>({
        initialValues: {
            message: '',
            provider: 'twitch',
            created_by_display_name: '',
            created_by_provider_viewer_id: '',
        },
    })

    return (
        <form
            onSubmit={form.onSubmit((values) => {
                create.mutate({
                    channelId,
                    data: values,
                })
            })}
        >
            <Flex direction={'column'} gap="1rem">
                <QuoteForm form={form} />

                <Flex>
                    <Button loading={create.isPending} ml="auto" type="submit">
                        Save
                    </Button>
                </Flex>
            </Flex>
        </form>
    )
}

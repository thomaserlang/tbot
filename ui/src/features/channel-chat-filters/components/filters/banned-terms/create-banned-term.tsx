import { ChatFilterId } from '@/features/channel-chat-filters/filter.types'
import { ChannelId } from '@/features/channel/types'
import { setFormErrors } from '@/utils/form'
import { Button, Flex } from '@mantine/core'
import { useForm } from '@mantine/form'
import { BannedTermForm } from './banned-term-form'
import { useCreateBannedTerm } from './banned-term.api'
import { BannedTerm, BannedTermRequest } from './banned-terms.types'

interface Props {
    channelId: ChannelId
    filterId: ChatFilterId
    onCreated?: (term: BannedTerm) => void
}

export function CreateBannedTerm({ channelId, filterId, onCreated }: Props) {
    const create = useCreateBannedTerm({
        onSuccess: (data) => {
            onCreated?.(data)
            close()
        },
        onError: (error) => {
            if (error.status === 422) setFormErrors(form, error.response.data)
        },
    })

    const form = useForm<BannedTermRequest>({
        initialValues: {
            type: 'phrase',
            text: '',
        },
    })

    return (
        <form
            onSubmit={form.onSubmit((values) => {
                create.mutate({
                    channelId,
                    chatFilterId: filterId,
                    data: values,
                })
            })}
        >
            <Flex gap="1rem" direction="column">
                <BannedTermForm form={form} />

                <Flex>
                    <Button ml="auto" type="submit" loading={create.isPending}>
                        Save
                    </Button>
                </Flex>
            </Flex>
        </form>
    )
}

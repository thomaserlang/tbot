import { ChannelId } from '@/features/channel/types/channel.types'
import { setFormErrors } from '@/utils/form'
import { Button, Flex } from '@mantine/core'
import { useForm } from '@mantine/form'
import { BannedTermForm } from './banned-term-form'
import { useUpdateBannedTerm } from './banned-term.api'
import { BannedTerm, BannedTermRequest } from './banned-terms.types'

interface Props {
    channelId: ChannelId
    bannedTerm: BannedTerm
    onUpdated?: (term: BannedTerm) => void
}

export function EditBannedTerm({ channelId, bannedTerm, onUpdated }: Props) {
    const update = useUpdateBannedTerm({
        onSuccess: (data) => {
            onUpdated?.(data)
            close()
        },
        onError: (error) => {
            if (error.status === 422) setFormErrors(form, error.response.data)
        },
    })

    const form = useForm<BannedTermRequest>({
        initialValues: {
            type: bannedTerm.type,
            text: bannedTerm.text,
        },
    })

    return (
        <form
            onSubmit={form.onSubmit((values) => {
                update.mutate({
                    channelId,
                    chatFilterId: bannedTerm.chat_filter_id,
                    bannedTermId: bannedTerm.id,
                    data: values,
                })
            })}
        >
            <Flex gap="1rem" direction="column">
                <BannedTermForm form={form} />

                <Flex>
                    <Button ml="auto" type="submit" loading={update.isPending}>
                        Save
                    </Button>
                </Flex>
            </Flex>
        </form>
    )
}

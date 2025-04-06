import { ChannelId } from '@/features/channel/types'
import { Button, Flex } from '@mantine/core'
import { useForm } from '@mantine/form'
import { AxiosError } from 'axios'
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
                        Update
                    </Button>
                </Flex>
            </Flex>
        </form>
    )
}

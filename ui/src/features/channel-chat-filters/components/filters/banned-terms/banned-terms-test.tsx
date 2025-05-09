import {
    ChatFilterId,
    ChatFilterMatchResult,
} from '@/features/channel-chat-filters/filter.types'
import { ChannelId } from '@/features/channel/types/channel.types'
import { toastError } from '@/utils/toast'
import { Button, Flex, Text, TextInput } from '@mantine/core'
import { useForm } from '@mantine/form'
import { useTestBannedTerms } from './banned-terms.api'

interface Props {
    channelId: ChannelId
    chatFilterId: ChatFilterId
    value?: ChatFilterMatchResult | null
    onChange?: (matchResult: ChatFilterMatchResult | null) => void
}

export function BannedTermsTest({
    channelId,
    chatFilterId,
    value,
    onChange,
}: Props) {
    const test = useTestBannedTerms({
        onSuccess: (data) => {
            onChange?.(data)
        },
        onError: (error) => {
            toastError(error)
        },
    })

    const form = useForm({
        initialValues: {
            message: '',
        },
        onValuesChange: () => {
            test.reset()
            onChange?.(null)
        },
    })
    return (
        <form
            onSubmit={form.onSubmit((values) => {
                test.mutate({
                    channelId,
                    chatFilterId,
                    message: values.message,
                })
            })}
        >
            <Flex gap="0.5rem" align="center">
                <TextInput
                    placeholder="Type a message to test"
                    key={form.key('message')}
                    {...form.getInputProps('message')}
                />

                <Button
                    variant="default"
                    loading={test.isPending}
                    color="teal"
                    type="submit"
                >
                    Test
                </Button>

                {value && (
                    <Text size="sm" c={value.matched ? 'teal' : 'red'} fw={500}>
                        {value.matched ? 'Matched' : "Didn't Matched"}
                    </Text>
                )}
            </Flex>
        </form>
    )
}

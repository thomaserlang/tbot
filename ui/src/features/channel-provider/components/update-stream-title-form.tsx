import { providerInfo } from '@/constants'
import { toastPromise } from '@/utils/toast'
import { Button, Flex, Switch, Text, Textarea } from '@mantine/core'
import { useForm } from '@mantine/form'
import { useUpdateStreamTitle } from '../api/channel-provider-stream-title.api'
import { useGetChannelProviders } from '../api/channel-providers.api'
import { ChannelProvider } from '../channel-provider.types'

interface Props {
    channelProvider: ChannelProvider
    onClose?: () => void
}

export function UpdateStreamTitleForm({ channelProvider, onClose }: Props) {
    const channelProviders = useGetChannelProviders({
        channelId: channelProvider.channel_id,
    })
    const update = useUpdateStreamTitle()
    const form = useForm({
        initialValues: {
            update_all: true,
            stream_title: channelProvider.stream_title || '',
        },
        validate: {
            stream_title: (value) =>
                value.length < 1 ? 'Title is required' : null,
        },
    })

    return (
        <form
            onSubmit={form.onSubmit((values) => {
                for (const p of channelProviders.data?.filter(
                    (f) => providerInfo[f.provider].streamTitleMaxLength
                ) || []) {
                    if (!form.values.update_all && p.id !== channelProvider.id)
                        continue
                    toastPromise({
                        promise: update.mutateAsync({
                            channelId: p.channel_id,
                            channelProviderId: p.id,
                            data: {
                                stream_title: values.stream_title,
                            },
                        }),
                        loading: {
                            title: providerInfo[p.provider].name,
                            message: `Updating stream title`,
                        },
                        success: {
                            title: providerInfo[p.provider].name,
                            message: `Stream title updated`,
                        },
                        error: {
                            title: providerInfo[p.provider].name,
                        },
                    })
                }
                onClose?.()
            })}
        >
            <Flex gap="0.5rem" direction="column">
                <Flex gap="0.10rem" direction="column">
                    <Textarea
                        autosize
                        minRows={3}
                        minLength={1}
                        maxLength={100}
                        w="100%"
                        key={form.key('stream_title')}
                        readOnly={update.isPending}
                        data-autofocus
                        {...form.getInputProps('stream_title')}
                    />
                    <Text size="sm" c="dimmed" ml="auto">
                        {form.values.stream_title.length}/
                        {providerInfo[channelProvider.provider]
                            .streamTitleMaxLength || 100}
                    </Text>
                </Flex>
                <Flex gap="0.5rem" align="center">
                    <Switch
                        label="Update title for all live streams"
                        {...form.getInputProps('update_all', {
                            type: 'checkbox',
                        })}
                    />
                    <Button ml="auto" type="submit" loading={update.isPending}>
                        Update
                    </Button>
                </Flex>
            </Flex>
        </form>
    )
}

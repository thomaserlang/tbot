import { PageLoader } from '@/components/page-loader'
import { ChatView } from '@/features/channel-chat'
import { useCurrentChannel } from '@/features/channel/current-channel.provider'
import { Feature } from '@/types/feature.type'
import { Provider } from '@/types/provider.type'
import { strDateFormat } from '@/utils/date'
import { Box, Divider, Flex, Modal, Paper, Text } from '@mantine/core'
import humanizeDuration from 'humanize-duration'
import { useGetChannelViewer } from '../api/channel-viewer'
import { ProviderViewerId } from '../types/viewer.type'
import { ModerationButtons } from './moderation-buttons'
import { ViewerStreamsTable } from './viewer-streams-table'

interface Props {
    provider: Provider
    providerViewerId: ProviderViewerId
}

const hourHumanizer = humanizeDuration.humanizer({
    units: ['h', 'm'],
    largest: 1,
    language: 'short',
    maxDecimalPoints: 0,
    languages: {
        short: {
            h: () => 'h',
            m: () => 'm',
        },
    },
    spacer: '',
})

export function ChannelViewerView(props: Props) {
    const channel = useCurrentChannel()
    const { data, isLoading } = useGetChannelViewer({
        ...props,
        channelId: channel.id,
    })
    if (isLoading) return <PageLoader />
    if (!data) return null

    return (
        <Flex gap="1rem" direction="column">
            <Flex gap="1rem" justify="space-between">
                <Divider orientation="vertical" />

                <Flex direction="column" align="center">
                    <Text fz={24}>{data.stats.streams}</Text>
                    <Text fz={12} fw={700} tt="capitalize">
                        Streams
                    </Text>
                </Flex>

                <Divider orientation="vertical" />

                {channel.features.includes(
                    Feature.CHANNEL_VIEWER_EXTRA_STATS
                ) && (
                    <>
                        <Flex direction="column" align="center">
                            <Text fz={24}>
                                {data.stats.last_channel_provider_stream
                                    ? strDateFormat(
                                          data.stats
                                              .last_channel_provider_stream
                                              .started_at
                                      )
                                    : 'N/A'}
                            </Text>
                            <Text fz={12} fw={700} tt="capitalize">
                                Last stream
                            </Text>
                        </Flex>
                        <Divider orientation="vertical" />
                    </>
                )}

                <Flex direction="column" align="center">
                    <Text fz={24}>
                        {hourHumanizer(data.stats.watchtime * 1000)}
                    </Text>
                    <Text fz={12} fw={700} tt="capitalize">
                        Watchtime
                    </Text>
                </Flex>

                <Divider orientation="vertical" />
            </Flex>

            <ModerationButtons
                channelId={channel.id}
                provider={props.provider}
                providerViewerId={props.providerViewerId}
            />

            <Box>
                <Text fw={700}>Chatlog</Text>
                <Paper h="15rem" pl="0.5rem" withBorder>
                    <ChatView
                        channelId={channel.id}
                        liveUpdates={true}
                        params={{
                            provider: props.provider,
                            provider_viewer_id: props.providerViewerId,
                        }}
                    />
                </Paper>
            </Box>

            {channel.features.includes(Feature.CHANNEL_VIEWER_EXTRA_STATS) &&
                data.stats.last_channel_provider_stream && (
                    <Box>
                        <Text fw={700}>Streams</Text>
                        <Box mah={400}>
                            <ViewerStreamsTable
                                channelId={channel.id}
                                provider={props.provider}
                                providerViewerId={props.providerViewerId}
                            />
                        </Box>
                    </Box>
                )}
        </Flex>
    )
}

interface ModalProps extends Props {
    opened: boolean
    onClose: () => void
}

export function ChannelViewerModal(props: ModalProps) {
    const channel = useCurrentChannel()
    const { data } = useGetChannelViewer({ ...props, channelId: channel.id })

    return (
        <Modal
            opened={props.opened}
            onClose={props.onClose}
            title={data ? data.viewer.display_name : ''}
        >
            <ChannelViewerView {...props} />
        </Modal>
    )
}

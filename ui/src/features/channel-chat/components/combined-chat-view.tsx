import {
    RunCommercialButton,
    UpdateStreamTitleButton,
} from '@/features/channel-provider'
import {
    ChannelViewerModal,
    ViewerName,
    ViewerSearchButton,
} from '@/features/channel-viewer'
import { ChannelId } from '@/features/channel/types/channel.types'
import { Box, Divider, Flex, Paper } from '@mantine/core'
import { useState } from 'react'
import { ChatView } from './chat-view'
import { CombinedChatHeader } from './combined-chat-header'

interface Props {
    channelId: ChannelId
    hideChannelProviders?: boolean
}

export function CombinedChatView({ channelId, hideChannelProviders }: Props) {
    const [showViewer, setShowViewer] = useState<ViewerName | null>(null)

    return (
        <>
            <Flex direction="column" h="100%" w="100%">
                <Paper>
                    <Paper p="0.25rem 0.5rem">
                        <CombinedChatHeader
                            hideChannelProviders={hideChannelProviders}
                        />
                    </Paper>
                    <Divider />
                </Paper>

                <Paper h="100%">
                    <ChatView
                        channelId={channelId}
                        onViewerClick={(viewer) => {
                            setShowViewer(viewer)
                        }}
                    />
                </Paper>

                <Divider />

                <Box p="0.5rem">
                    <Flex gap="0.5rem">
                        <RunCommercialButton channelId={channelId} />
                        <UpdateStreamTitleButton channelId={channelId} />
                        <Flex ml="auto" gap="0.5rem" align="center">
                            <ViewerSearchButton
                                onSelect={(viewer) => setShowViewer(viewer)}
                            />
                        </Flex>
                    </Flex>
                </Box>
            </Flex>

            {showViewer && (
                <ChannelViewerModal
                    provider={showViewer.provider}
                    providerViewerId={showViewer.provider_viewer_id}
                    opened={true}
                    onClose={() => {
                        setShowViewer(null)
                    }}
                />
            )}
        </>
    )
}

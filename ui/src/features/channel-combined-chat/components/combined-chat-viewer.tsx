import {
    ChannelViewerModal,
    ViewerName,
    ViewerSearchButton,
} from '@/features/channel-viewer'
import { ChannelId } from '@/features/channel/types'
import { Box, Divider, Flex, Title } from '@mantine/core'
import { useState } from 'react'
import { ChatViewer } from './chat-viewer'

interface Props {
    channelId: ChannelId
    hideTitle?: boolean
}

export function CombinedChatViewer({ channelId, hideTitle }: Props) {
    const [showViewer, setShowViewer] = useState<ViewerName | null>(null)

    return (
        <>
            <Flex direction="column" h="100%" w="100%" gap="0.5rem">
                {!hideTitle && (
                    <Flex>
                        <Title order={2}>Combined Chat</Title>
                    </Flex>
                )}

                <ChatViewer
                    channelId={channelId}
                    onViewerClick={(viewer) => {
                        setShowViewer(viewer)
                    }}
                />

                <Divider />

                <Flex>
                    <Box ml="auto">
                        <ViewerSearchButton
                            onSelect={(viewer) => {
                                setShowViewer(viewer)
                            }}
                        />
                    </Box>
                </Flex>
            </Flex>

            {showViewer && (
                <ChannelViewerModal
                    channelId={channelId}
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

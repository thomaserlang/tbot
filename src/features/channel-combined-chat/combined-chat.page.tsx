import { useCurrentChannel } from '@/features/channel/current-channel.provider'
import { useDocumentTitle } from '@/utils/document-title'
import { Box, Container, Flex, Title } from '@mantine/core'
import { useState } from 'react'
import { ViewerSearchButton } from '../channel-viewer'
import { ChannelViewerModal } from '../channel-viewer/components/channel-viewer-view'
import { ViewerName } from '../channel-viewer/types/viewer.type'
import { ChatViewer } from './components/chat-viewer'

export function Component() {
    const channel = useCurrentChannel()
    const [showViewer, setShowViewer] = useState<ViewerName | null>(null)
    useDocumentTitle(`Combined Chat - ${channel.display_name}`)

    return (
        <Container size="lg">
            <Flex direction="column" h="var(--tbot-content-height)" gap="1rem">
                <Flex>
                    <Title order={2}>Combined Chat</Title>

                    <Box ml="auto">
                        <ViewerSearchButton
                            onSelect={(viewer) => {
                                setShowViewer(viewer)
                            }}
                        />
                    </Box>
                </Flex>

                <ChatViewer
                    channelId={channel.id}
                    onViewerClick={(viewer) => {
                        setShowViewer(viewer)
                    }}
                />
            </Flex>

            {showViewer && (
                <ChannelViewerModal
                    channelId={channel.id}
                    provider={showViewer.provider}
                    viewerId={showViewer.provider_viewer_id}
                    opened={true}
                    onClose={() => {
                        setShowViewer(null)
                    }}
                />
            )}
        </Container>
    )
}

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
import { ActionIcon, Divider, Flex, Title } from '@mantine/core'
import { IconDotsVertical } from '@tabler/icons-react'
import { useState } from 'react'
import { ChatMenu } from './chat-menu'
import { ChatView } from './chat-view'

interface Props {
    channelId: ChannelId
    hideTitle?: boolean
}

export function CombinedChatView({ channelId, hideTitle }: Props) {
    const [showViewer, setShowViewer] = useState<ViewerName | null>(null)

    return (
        <>
            <Flex direction="column" h="100%" w="100%" gap="0.5rem">
                {!hideTitle && (
                    <Flex>
                        <Title order={2}>Combined Chat</Title>
                    </Flex>
                )}

                <ChatView
                    channelId={channelId}
                    onViewerClick={(viewer) => {
                        setShowViewer(viewer)
                    }}
                />

                <Divider />

                <Flex gap="0.5rem">
                    <RunCommercialButton channelId={channelId} />
                    <UpdateStreamTitleButton channelId={channelId} />
                    <Flex ml="auto" gap="0.5rem" align="center">
                        <ViewerSearchButton
                            onSelect={(viewer) => {
                                setShowViewer(viewer)
                            }}
                        />
                        <ChatMenu>
                            <ActionIcon variant="subtle" color="gray">
                                <IconDotsVertical
                                    style={{ width: '70%', height: '70%' }}
                                />
                            </ActionIcon>
                        </ChatMenu>
                    </Flex>
                </Flex>
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

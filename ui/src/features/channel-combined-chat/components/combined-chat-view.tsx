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
import { ActionIcon, Divider, Flex, Paper, ScrollArea } from '@mantine/core'
import { IconDotsVertical } from '@tabler/icons-react'
import { useState } from 'react'
import { ChatMenu } from './chat-menu'
import { ChatView } from './chat-view'
import { CombinedChatHeader } from './combined-chat-header'

interface Props {
    channelId: ChannelId
    hideHeader?: boolean
}

export function CombinedChatView({ channelId, hideHeader }: Props) {
    const [showViewer, setShowViewer] = useState<ViewerName | null>(null)

    return (
        <>
            <Flex direction="column" h="100%" w="100%">
                {!hideHeader && (
                    <Paper>
                        <Paper p="0.25rem 0.5rem">
                            <CombinedChatHeader />
                        </Paper>
                        <Divider />
                    </Paper>
                )}

                <Paper pl="0.25rem" pb="0.5rem" h="100%">
                    <ChatView
                        channelId={channelId}
                        onViewerClick={(viewer) => {
                            setShowViewer(viewer)
                        }}
                    />
                </Paper>

                <Divider />

                <Paper p="0.5rem 0 0.5rem 0.5rem">
                    <ScrollArea>
                        <Flex gap="0.5rem">
                            <RunCommercialButton channelId={channelId} />
                            <UpdateStreamTitleButton channelId={channelId} />
                            <Flex ml="auto" gap="0.5rem" align="center">
                                <ViewerSearchButton
                                    onSelect={(viewer) => setShowViewer(viewer)}
                                />
                                <ChatMenu>
                                    <ActionIcon variant="subtle" color="gray">
                                        <IconDotsVertical
                                            style={{
                                                width: '70%',
                                                height: '70%',
                                            }}
                                        />
                                    </ActionIcon>
                                </ChatMenu>
                            </Flex>
                        </Flex>
                    </ScrollArea>
                </Paper>
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

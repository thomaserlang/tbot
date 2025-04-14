import { useCurrentChannel } from '@/features/channel/current-channel.provider'
import { useDocumentTitle } from '@/utils/document-title'
import { Container, Flex } from '@mantine/core'
import { ChatlogsViewer } from './components/chat-viewer'

export function Component() {
    const channel = useCurrentChannel()
    useDocumentTitle(`Combined Chat - ${channel.display_name}`)

    return (
        <Container size="lg">
            <Flex direction="column" h="var(--tbot-content-height)">
                <ChatlogsViewer channelId={channel.id} />
            </Flex>
        </Container>
    )
}

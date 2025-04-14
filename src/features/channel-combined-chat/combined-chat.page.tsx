import { useCurrentChannel } from '@/features/channel/current-channel.provider'
import { Container, Flex } from '@mantine/core'
import { ChatlogsViewer } from './components/chat-viewer'

export function Component() {
    const channel = useCurrentChannel()
    return (
        <Container size="lg">
            <Flex direction="column" h="var(--tbot-content-height)">
                <ChatlogsViewer channelId={channel.id} />
            </Flex>
        </Container>
    )
}

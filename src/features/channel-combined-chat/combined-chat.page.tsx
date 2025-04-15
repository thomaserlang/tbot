import { useCurrentChannel } from '@/features/channel/current-channel.provider'
import { useDocumentTitle } from '@/utils/document-title'
import { Container, Flex, Title } from '@mantine/core'
import { ChatViewer } from './components/chat-viewer'

export function Component() {
    const channel = useCurrentChannel()
    useDocumentTitle(`Combined Chat - ${channel.display_name}`)

    return (
        <Container size="lg">
            <Flex direction="column" h="var(--tbot-content-height)" gap="1rem">
                <Flex>
                    <Title order={2}>Combined Chat</Title>
                </Flex>

                <ChatViewer channelId={channel.id} />
            </Flex>
        </Container>
    )
}

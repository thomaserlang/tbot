import { useCurrentChannel } from '@/features/channel/current-channel.provider'
import { useDocumentTitle } from '@/utils/document-title'
import { Container } from '@mantine/core'
import { CombinedChatViewer } from './components/combined-chat-viewer'

export function Component() {
    const channel = useCurrentChannel()
    useDocumentTitle(`Combined Chat - ${channel.display_name}`)

    return (
        <Container size="lg" h="var(--tbot-content-height)">
            <CombinedChatViewer channelId={channel.id} />
        </Container>
    )
}

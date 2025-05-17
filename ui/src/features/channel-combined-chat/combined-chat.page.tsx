import { useCurrentChannel } from '@/features/channel/current-channel.provider'
import { useDocumentTitle } from '@/utils/document-title'
import { Paper } from '@mantine/core'
import { CombinedChatView } from './components/combined-chat-view'

export function Component() {
    const channel = useCurrentChannel()
    useDocumentTitle(`Combined Chat - ${channel.display_name}`)

    return (
        <Paper withBorder h="var(--tbot-content-height)">
            <CombinedChatView channelId={channel.id} />
        </Paper>
    )
}

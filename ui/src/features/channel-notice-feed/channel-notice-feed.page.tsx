import { useCurrentChannel } from '@/features/channel/current-channel.provider'
import { useDocumentTitle } from '@/utils/document-title'
import { Paper } from '@mantine/core'
import { NoticeFeedView } from './components/notice-feed-view'

export function Component() {
    const channel = useCurrentChannel()
    useDocumentTitle(`Notice Feed - ${channel.display_name}`)

    return (
        <Paper withBorder h="var(--tbot-content-height)" p="0.5rem">
            <NoticeFeedView channelId={channel.id} />
        </Paper>
    )
}

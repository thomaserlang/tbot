import { useCurrentChannel } from '@/features/channel/current-channel.provider'
import { useDocumentTitle } from '@/utils/document-title'
import { Paper } from '@mantine/core'
import { NoticeFeedView } from './components/notice-feed-view'

export function Component() {
    const channel = useCurrentChannel()
    useDocumentTitle(`Notice Feed - ${channel.display_name}`)

    return (
        <Paper
            h="calc(var(--tbot-content-height) + 1rem)"
            mt="-1rem"
            ml="-1rem"
            mr="-1rem"
        >
            <NoticeFeedView channelId={channel.id} />
        </Paper>
    )
}

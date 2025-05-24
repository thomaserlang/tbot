import { useCurrentChannel } from '@/features/channel/current-channel.provider'
import { useDocumentTitle } from '@/utils/document-title'
import { Paper } from '@mantine/core'
import { ActivityFeedView } from './components/activity-feed-view'

export function Component() {
    const channel = useCurrentChannel()
    useDocumentTitle(`Activity Feed - ${channel.display_name}`)

    return (
        <Paper
            h="calc(var(--tbot-content-height) + var(--app-shell-padding))"
            mt="calc(var(--app-shell-padding) * -1)"
            ml="calc(var(--app-shell-padding) * -1)"
            mr="calc(var(--app-shell-padding) * -1)"
        >
            <ActivityFeedView channelId={channel.id} />
        </Paper>
    )
}

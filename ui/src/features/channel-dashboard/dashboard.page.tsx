import { useCurrentChannel } from '@/features/channel'
import { useDocumentTitle } from '@/utils/document-title'
import { Container, Flex, Paper } from '@mantine/core'
import { CombinedChatViewer } from '../channel-combined-chat'
import { NoticeFeedViewer } from '../channel-notice-feed'
import { DashboardProviders } from './components/dashboard-providers'

export function Component() {
    const channel = useCurrentChannel()
    useDocumentTitle(`Dashboard - ${channel.display_name}`)

    return (
        <Container size="xl">
            <Flex direction="column" h="var(--tbot-content-height)" gap="1rem">
                <DashboardProviders channelId={channel.id} />
                <Flex gap="1rem" flex={1}>
                    <Paper w={350} withBorder p="0.5rem" pr="0.25rem">
                        <NoticeFeedViewer channelId={channel.id} />
                    </Paper>

                    <Paper flex={1} withBorder p="0.5rem">
                        <CombinedChatViewer channelId={channel.id} hideTitle />
                    </Paper>
                </Flex>
            </Flex>
        </Container>
    )
}

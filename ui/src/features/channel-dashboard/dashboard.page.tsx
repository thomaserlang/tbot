import { useCurrentChannel } from '@/features/channel'
import { useDocumentTitle } from '@/utils/document-title'
import { Container, Flex, Paper } from '@mantine/core'
import { ActivityFeedView } from '../channel-activity'
import { CombinedChatView } from '../channel-chat'
import { DashboardProviders } from './components/dashboard-providers'

export function Component() {
    const channel = useCurrentChannel()
    useDocumentTitle(`Dashboard - ${channel.display_name}`)

    return (
        <Container size="xl">
            <Flex direction="column" h="var(--tbot-content-height)" gap="1rem">
                <DashboardProviders channelId={channel.id} />

                <Flex gap="1rem" flex={1} wrap={'wrap'}>
                    <Paper maw={400} flex={1} withBorder miw={300}>
                        <ActivityFeedView channelId={channel.id} />
                    </Paper>

                    <Paper flex={1} withBorder miw={300}>
                        <CombinedChatView
                            channelId={channel.id}
                            hideChannelProviders
                        />
                    </Paper>
                </Flex>
            </Flex>
        </Container>
    )
}

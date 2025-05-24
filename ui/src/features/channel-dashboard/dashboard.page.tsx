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
            <Flex
                direction="column"
                h="calc(var(--tbot-content-height) + var(--app-shell-padding))"
                gap="0.5rem"
                mt="calc(var(--app-shell-padding) * -1)"
                ml="calc(var(--app-shell-padding) * -1)"
                mr="calc(var(--app-shell-padding) * -1)"
            >
                <Paper p="0.5rem" radius="0">
                    <DashboardProviders channelId={channel.id} />
                </Paper>

                <Flex gap="0.5rem" flex={1} wrap={'wrap'}>
                    <Paper maw={400} flex={1} miw={300}>
                        <ActivityFeedView channelId={channel.id} />
                    </Paper>

                    <Paper flex={1} miw={300}>
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

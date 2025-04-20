import { useCurrentChannel } from '@/features/channel'
import { useDocumentTitle } from '@/utils/document-title'
import { Container } from '@mantine/core'
import { DashboardProviders } from './components/dashboard-providers'

export function Component() {
    const channel = useCurrentChannel()
    useDocumentTitle(`Dashboard - ${channel.display_name}`)

    return (
        <Container size="xl">
            <DashboardProviders channelId={channel.id} />
        </Container>
    )
}

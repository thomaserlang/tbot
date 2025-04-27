import { Container, Title } from '@mantine/core'
import { useCurrentChannel } from '../channel/current-channel.provider'
import { ChannelPointSettingsView } from './components/channel-point-settings-view'

export function Component() {
    const channel = useCurrentChannel()

    return (
        <>
            <title>Points Settings</title>
            <Container size="xs">
                <Title order={2} mb="md">
                    Points Settings
                </Title>
                <ChannelPointSettingsView channelId={channel.id} />
            </Container>
        </>
    )
}

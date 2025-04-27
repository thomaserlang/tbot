import { Container, Title } from '@mantine/core'
import { useCurrentChannel } from '../channel/current-channel.provider'
import { SlotsSettingsView } from './components/slots-settings-view'

export function Component() {
    const channel = useCurrentChannel()

    return (
        <>
            <title>Slots Settings</title>
            <Container size="xs">
                <Title order={2} mb="md">
                    Slots Settings
                </Title>
                <SlotsSettingsView channelId={channel.id} />
            </Container>
        </>
    )
}

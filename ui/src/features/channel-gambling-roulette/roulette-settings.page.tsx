import { Container, Title } from '@mantine/core'
import { useCurrentChannel } from '../channel/current-channel.provider'
import { RouletteSettingsView } from './components/roulette-settings-view'

export function Component() {
    const channel = useCurrentChannel()

    return (
        <>
            <title>Roulette Settings</title>
            <Container size="xs">
                <Title order={2} mb="md">
                    Roulette Settings
                </Title>
                <RouletteSettingsView channelId={channel.id} />
            </Container>
        </>
    )
}

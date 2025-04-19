import { Flex, Title } from '@mantine/core'
import { ChannelProvider } from '../channel-provider.types'
import { BotButtonAction } from './bot-button-action'
import { ButtonAction } from './button-action'

interface Props {
    provider: ChannelProvider
    onDeleted?: () => void
}

export function ProviderView({ provider, onDeleted }: Props) {
    return (
        <Flex gap="1rem" direction="column">
            <ButtonAction provider={provider} onDeleted={onDeleted} />

            {['twitch', 'youtube'].includes(provider.provider) && (
                <Flex gap="0.25rem" direction="column">
                    <Title order={5}>Your own bot</Title>
                    <BotButtonAction provider={provider} />
                </Flex>
            )}
        </Flex>
    )
}

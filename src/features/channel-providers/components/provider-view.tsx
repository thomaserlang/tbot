import { Flex, Title } from '@mantine/core'
import { ChannelProvider } from '../provider.types'
import { BotButtonAction } from './bot-button-action'
import { ButtonAction } from './button-action'

interface Props {
    provider: ChannelProvider
}

export function ProviderView({ provider }: Props) {
    return (
        <Flex gap="1rem" direction="column">
            <ButtonAction provider={provider} />

            {provider.provider == 'twitch' && (
                <Flex gap="0.25rem" direction="column">
                    <Title order={5}>Your own bot</Title>
                    <BotButtonAction provider={provider} />
                </Flex>
            )}
        </Flex>
    )
}

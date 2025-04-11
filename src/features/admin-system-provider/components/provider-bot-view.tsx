import { ProviderBot } from '@/features/provider-bot/provider-bot.types'
import { Flex } from '@mantine/core'
import { ButtonAction } from './button-action'

interface Props {
    provider: ProviderBot
    onDeleted?: () => void
}

export function ProviderBotView({ provider, onDeleted }: Props) {
    return (
        <Flex gap="1rem" direction="column">
            <ButtonAction provider={provider} onDeleted={onDeleted} />
        </Flex>
    )
}

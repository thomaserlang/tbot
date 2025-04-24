import { providerInfo } from '@/constants'
import { ProviderBot } from '@/features/provider-bot/provider-bot.types'
import { Button, Flex, Paper, Text } from '@mantine/core'
import { IconRobot } from '@tabler/icons-react'
import { useNavigate } from 'react-router-dom'

interface Props {
    providerBots: ProviderBot[]
}

export function ProviderBotsView({ providerBots }: Props) {
    const navigate = useNavigate()

    if (providerBots.length === 0) {
        return (
            <Flex justify="center" align="center" direction="column" gap="1rem">
                <IconRobot size={40} />
                <Text fw={500}>No system provider bots found, add one.</Text>
            </Flex>
        )
    }

    return (
        <Flex gap="2rem" wrap={'wrap'}>
            {providerBots.map((bot) => (
                <Paper key={bot.id} withBorder p="0.5rem" w={300}>
                    <Text fw={500} size="lg">
                        {providerInfo[bot.provider].name || bot.provider}
                    </Text>

                    <Flex gap="0.5rem" align="center">
                        <Text c="dimmed">{bot.name}</Text>

                        <Button
                            ml="auto"
                            size="xs"
                            variant="outline"
                            rightSection={bot.scope_needed}
                            onClick={() => {
                                navigate(
                                    `/admin/system-provider-bots/${bot.provider}`
                                )
                            }}
                        >
                            Settings
                        </Button>
                    </Flex>
                </Paper>
            ))}
        </Flex>
    )
}

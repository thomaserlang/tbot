import { providerLabels } from '@/types/provider.type'
import { Badge, Button, Flex, Paper, Text } from '@mantine/core'
import { useNavigate } from 'react-router-dom'
import { ChannelProvider } from '../provider.types'

interface Props {
    providers: ChannelProvider[]
}

export function ProvidersView({ providers }: Props) {
    const navigate = useNavigate()
    return (
        <Flex gap="2rem" wrap={'wrap'}>
            {providers.map((provider) => (
                <Paper key={provider.id} withBorder p="0.5rem" w={300}>
                    <Text fw={500} size="lg">
                        {providerLabels[provider.provider] || provider.provider}
                    </Text>

                    <Flex gap="0.5rem" align="center">
                        <Text c="dimmed">{provider.name}</Text>

                        <Button
                            ml="auto"
                            size="xs"
                            variant="outline"
                            rightSection={
                                provider.scope_needed && (
                                    <Badge
                                        size="xs"
                                        color="red"
                                        title="Extra scope required"
                                    >
                                        1
                                    </Badge>
                                )
                            }
                            onClick={() => {
                                navigate(
                                    `/channels/${provider.channel_id}/providers/${provider.id}`
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

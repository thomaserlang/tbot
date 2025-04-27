import { providerInfo } from '@/constants'
import { Badge, Button, Flex, Paper, Text } from '@mantine/core'
import { IconLink } from '@tabler/icons-react'
import { useNavigate } from 'react-router-dom'
import { ChannelProvider } from '../channel-provider.types'

interface Props {
    channelProviders: ChannelProvider[]
}

export function ProvidersView({ channelProviders: channelProviders }: Props) {
    const navigate = useNavigate()

    if (channelProviders.length === 0) {
        return (
            <Flex justify="center" align="center" direction="column" gap="1rem">
                <IconLink size={80} />
                <Text size="xl" fw={500}>
                    No providers found, add one.
                </Text>
            </Flex>
        )
    }

    return (
        <Flex gap="1rem" wrap={'wrap'}>
            {channelProviders.map((channelProvider) => (
                <Paper key={channelProvider.id} withBorder p="0.5rem" w={300}>
                    <Text fw={500} size="lg">
                        {providerInfo[channelProvider.provider].name ||
                            channelProvider.provider}
                    </Text>

                    <Flex gap="0.5rem" align="center">
                        <Text c="dimmed">
                            {channelProvider.provider_user_display_name}
                        </Text>

                        <Button
                            ml="auto"
                            size="xs"
                            variant="outline"
                            rightSection={providerErrors(channelProvider)}
                            onClick={() => {
                                navigate(
                                    `/channels/${channelProvider.channel_id}/providers/${channelProvider.id}`
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

function providerErrors(provider: ChannelProvider) {
    let warnings = 0
    if (provider.scope_needed) warnings++
    if (provider.bot_provider?.scope_needed) warnings++
    if (warnings === 0) return null
    return (
        <Badge size="xs" color="red" title="Extra permissions required">
            {warnings}
        </Badge>
    )
}

import { useCurrentChannel } from '@/features/channel'
import { Box, Container, Flex, Paper, Text, Title } from '@mantine/core'
import { DeleteChannelButton } from './components/delete-channel-button'

export function Component() {
    const channel = useCurrentChannel()

    return (
        <Container size="xs">
            <Flex mb="1rem">
                <Title order={2}>Channel Settings</Title>
            </Flex>

            <Flex direction="column" gap="1rem">
                <Box>
                    <Text fw={500} size="xl">
                        Danger Zone
                    </Text>
                    <Paper withBorder p="1rem">
                        <Flex align="center">
                            <Box>
                                <Text fw={500}>Delete channel</Text>
                                <Text c="dimmed">
                                    There is no going back after this.
                                </Text>
                            </Box>
                            <Box ml="auto">
                                <DeleteChannelButton channelId={channel.id} />
                            </Box>
                        </Flex>
                    </Paper>
                </Box>
            </Flex>
        </Container>
    )
}

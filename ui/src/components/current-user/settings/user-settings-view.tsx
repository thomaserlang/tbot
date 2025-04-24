import { Box, Flex, Paper, Text } from '@mantine/core'
import { DeleteUserButton } from './components/delete-user-button'

export function UserSettingsView() {
    return (
        <>
            <Flex direction="column" gap="1rem">
                <Box>
                    <Text fw={500} size="xl">
                        Danger Zone
                    </Text>
                    <Paper withBorder p="1rem">
                        <Flex align="center">
                            <Box>
                                <Text fw={500}>Delete user profile</Text>
                                <Text c="dimmed">
                                    There is no going back after this.
                                </Text>
                            </Box>
                            <Box ml="auto">
                                <DeleteUserButton />
                            </Box>
                        </Flex>
                    </Paper>
                </Box>
            </Flex>
        </>
    )
}

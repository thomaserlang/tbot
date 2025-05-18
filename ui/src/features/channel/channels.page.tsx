import { CurrentUserCard, useCurrentUser } from '@/components/current-user'
import { Logo } from '@/components/logo'
import { SelectChannel } from '@/features/channel'
import { Container, Flex, Paper } from '@mantine/core'
import { Navigate, useNavigate } from 'react-router-dom'

export function Component() {
    const user = useCurrentUser()
    const navigate = useNavigate()
    if (user.default_channel_id) {
        return <Navigate to={`/channels/${user.default_channel_id}`} replace />
    }
    return (
        <Container size="xs" pt="0" p="1rem">
            <Flex h={50} mt="1rem" align="center" mb="1rem">
                <Logo />
                <Paper bg="none" ml="auto" p="0.3rem 0.5rem" withBorder>
                    <CurrentUserCard />
                </Paper>
            </Flex>
            <SelectChannel
                onSelect={(channel) => {
                    navigate(`/channels/${channel.id}`)
                }}
            />
        </Container>
    )
}

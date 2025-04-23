import { CurrentUserCard, useCurrentUser } from '@/components/current-user'
import { Logo } from '@/components/logo'
import { SelectChannel } from '@/features/channel'
import { Container, Flex } from '@mantine/core'
import { Navigate, useNavigate } from 'react-router-dom'

export function Component() {
    const user = useCurrentUser()
    const navigate = useNavigate()
    if (user.default_channel_id) {
        return <Navigate to={`/channels/${user.default_channel_id}`} />
    }
    return (
        <Container>
            <Flex h={50} align="center" mb="1rem">
                <Logo width="7rem" />
                <Flex ml="auto" mr="0.5rem">
                    <CurrentUserCard />
                </Flex>
            </Flex>
            <SelectChannel
                onSelect={(channel) => {
                    navigate(`/channels/${channel.id}`)
                }}
            />
        </Container>
    )
}

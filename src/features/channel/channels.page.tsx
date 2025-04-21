import { useCurrentUser } from '@/components/current-user'
import { SelectChannel } from '@/features/channel'
import { Container } from '@mantine/core'
import { Navigate, useNavigate } from 'react-router-dom'

export function Component() {
    const user = useCurrentUser()
    const navigate = useNavigate()
    if (user.default_channel_id) {
        return <Navigate to={`/channels/${user.default_channel_id}`} />
    }
    return (
        <Container>
            <SelectChannel
                onSelect={(channel) => {
                    navigate(`/channels/${channel.id}`)
                }}
            />
        </Container>
    )
}

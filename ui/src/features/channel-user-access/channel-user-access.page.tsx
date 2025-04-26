import { Container, Flex, Title } from '@mantine/core'
import { useCurrentChannel } from '../channel/current-channel.provider'
import { ChannelUserCreateInviteButton } from './components/channel-user-create-invite-button'
import { ChannelUserInvitesButton } from './components/channel-user-invites-button'
import { ChannelUsersAccessTable } from './components/channel-users-access-table'

export function Component() {
    const channel = useCurrentChannel()

    return (
        <>
            <title>User access</title>
            <Container size="xs">
                <Flex direction="column" gap="0.5rem">
                    <Flex gap="1rem">
                        <Title order={2}>Users with Access</Title>
                        <Flex gap="0.5rem" ml="auto">
                            <ChannelUserCreateInviteButton
                                channelId={channel.id}
                            />
                            <ChannelUserInvitesButton channelId={channel.id} />
                        </Flex>
                    </Flex>

                    <ChannelUsersAccessTable channelId={channel.id} />
                </Flex>
            </Container>
        </>
    )
}

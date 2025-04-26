import { CurrentUserCard } from '@/components/current-user'
import { ErrorBox } from '@/components/error-box'
import { Logo } from '@/components/logo'
import { PageLoader } from '@/components/page-loader'
import { Container, Flex, Paper, Text } from '@mantine/core'
import { useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { useAcceptChannelUserInvite } from './api/channel-user-invite.api'
import { ChannelUserInviteId } from './types/channel-user-invite.types'

export function Component() {
    const { channelUserInviteId } = useParams<{
        channelUserInviteId?: ChannelUserInviteId
    }>()
    const navigate = useNavigate()
    const acceptInvite = useAcceptChannelUserInvite({
        onSuccess: (channel) => {
            navigate(`/channels/${channel.id}`)
        },
    })

    useEffect(() => {
        if (channelUserInviteId) acceptInvite.mutate({ channelUserInviteId })
    }, [])

    return (
        <Container size="xs">
            <Flex h={50} mt="1rem" align="center" mb="1rem">
                <Logo width="7rem" />
                <Paper bg="none" ml="auto" p="0.3rem 0.5rem" withBorder>
                    <CurrentUserCard />
                </Paper>
            </Flex>
            <Flex direction="column" gap="1rem" justify="center" align="center">
                {!channelUserInviteId && (
                    <Text c="red" fw={500}>
                        Invalid invite link
                    </Text>
                )}
                {acceptInvite.isPending && (
                    <>
                        <Text fw={500}>Accepting invite</Text>
                        <PageLoader />
                    </>
                )}

                {acceptInvite.isSuccess && (
                    <Text c="green" fw={500}>
                        Invite accepted!
                    </Text>
                )}
                {acceptInvite.isError && (
                    <ErrorBox errorObj={acceptInvite.error} />
                )}
            </Flex>
        </Container>
    )
}

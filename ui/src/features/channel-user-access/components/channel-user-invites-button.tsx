import { ChannelId } from '@/features/channel/types/channel.types'
import { Button, Modal } from '@mantine/core'
import { useDisclosure } from '@mantine/hooks'
import { ChannelUserInvitesTable } from './channel-user-invites-table'

interface Props {
    channelId: ChannelId
}

export function ChannelUserInvitesButton({ channelId }: Props) {
    const [opened, { open, close }] = useDisclosure(false)

    return (
        <>
            <Button variant="default" onClick={open}>
                Invite links
            </Button>
            <Modal opened={opened} onClose={close} title="Invite links">
                {opened && <ChannelUserInvitesTable channelId={channelId} />}
            </Modal>
        </>
    )
}

import { ChannelId } from '@/features/channel/types/channel.types'
import { Button, Modal } from '@mantine/core'
import { useDisclosure } from '@mantine/hooks'
import { ChannelUserCreateInvite } from './channel-user-create-invite'

interface Props {
    channelId: ChannelId
}

export function ChannelUserCreateInviteButton({ channelId }: Props) {
    const [opened, { open, close }] = useDisclosure(false)

    return (
        <>
            <Button variant="light" onClick={open}>
                Create invite
            </Button>
            <Modal opened={opened} onClose={close} title="Create invite link">
                {opened && <ChannelUserCreateInvite channelId={channelId} />}
            </Modal>
        </>
    )
}

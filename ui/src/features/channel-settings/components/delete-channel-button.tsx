import { Button, Modal } from '@mantine/core'
import { useDisclosure } from '@mantine/hooks'
import { ChannelId } from '../../channel/types/channel.types'
import { DeleteChannelConfirm } from './delete-channel-confirm'

interface Props {
    channelId: ChannelId
}

export function DeleteChannelButton({ channelId }: Props) {
    const [opened, { open, close }] = useDisclosure(false)

    return (
        <>
            <Button variant="outline" color="red" onClick={open}>
                Delete this channel
            </Button>

            <Modal title="Delete channel" opened={opened} onClose={close}>
                {opened && <DeleteChannelConfirm channelId={channelId} />}
            </Modal>
        </>
    )
}

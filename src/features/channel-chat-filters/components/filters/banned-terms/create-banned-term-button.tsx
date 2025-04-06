import { ChatFilterId } from '@/features/channel-chat-filters/filter.types'
import { ChannelId } from '@/features/channel/types'
import { Button, Modal } from '@mantine/core'
import { useDisclosure } from '@mantine/hooks'
import { IconPlus } from '@tabler/icons-react'
import { BannedTerm } from './banned-terms.types'
import { CreateBannedTerm } from './create-banned-term'

interface Props {
    channelId: ChannelId
    chatFilterId: ChatFilterId
    onCreated?: (term: BannedTerm) => void
}

export function CreateBannedTermButton(props: Props) {
    const [opened, { open, close }] = useDisclosure(false)

    return (
        <>
            <Button
                onClick={open}
                variant="outline"
                leftSection={<IconPlus size={16} />}
            >
                Banned Term
            </Button>

            <Modal opened={opened} onClose={close} title="Create Banned Term">
                <CreateBannedTerm
                    channelId={props.channelId}
                    filterId={props.chatFilterId}
                    onCreated={(term) => {
                        props.onCreated?.(term)
                        close()
                    }}
                />
            </Modal>
        </>
    )
}

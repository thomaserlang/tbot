import { ChannelId } from '@/features/channel/types/channel.types'
import { Button, Modal } from '@mantine/core'
import { useDisclosure } from '@mantine/hooks'
import { IconPlus } from '@tabler/icons-react'
import { ChannelQuote } from '../types/quote.types'
import { QuoteCreateForm } from './quote-create-form'

interface Props {
    channelId: ChannelId
    onCreated?: (quote: ChannelQuote) => void
}

export function CreateQuoteButton({ channelId, onCreated }: Props) {
    const [opened, { open, close }] = useDisclosure(false)
    return (
        <>
            <Button
                ml="auto"
                variant="light"
                leftSection={<IconPlus size={14} />}
                onClick={open}
            >
                Create Quote
            </Button>

            <Modal
                size="md"
                opened={opened}
                onClose={close}
                title="Create Quote"
            >
                {opened && (
                    <QuoteCreateForm
                        channelId={channelId}
                        onCreated={(quote) => {
                            onCreated?.(quote)
                            close()
                        }}
                    />
                )}
            </Modal>
        </>
    )
}

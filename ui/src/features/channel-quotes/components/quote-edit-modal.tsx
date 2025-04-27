import { ErrorBox } from '@/components/error-box'
import { PageLoader } from '@/components/page-loader'
import { ChannelId } from '@/features/channel'
import { Modal } from '@mantine/core'
import { useGetQuote } from '../api/quote.api'
import { ChannelQuoteId } from '../types/quote.types'
import { EditQuoteForm } from './quote-edit-form'

interface Props {
    channelId: ChannelId
    channelQuoteId: ChannelQuoteId
    onClose: () => void
}

export function EditQuoteModal({ channelId, channelQuoteId, onClose }: Props) {
    const { isLoading, error, data } = useGetQuote({
        channelId,
        channelQuoteId,
    })
    return (
        <Modal
            size="md"
            opened={!!channelQuoteId}
            onClose={onClose}
            title="Edit Quote"
        >
            {isLoading && <PageLoader />}
            {error && <ErrorBox errorObj={error} />}
            {data && (
                <EditQuoteForm
                    quote={data}
                    onUpdated={() => {
                        onClose()
                    }}
                />
            )}
        </Modal>
    )
}

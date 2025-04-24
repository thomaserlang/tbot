import { ErrorBox } from '@/components/error-box'
import { PageLoader } from '@/components/page-loader'
import { ChannelId } from '@/features/channel'
import { Modal } from '@mantine/core'
import { useGetChatFilter } from '../filter.api'
import { ChatFilterId } from '../filter.types'
import { EditFilter } from './edit-filter'

interface Props {
    channelId: ChannelId
    filterId: ChatFilterId
    onClose: () => void
}

export function EditFilterModal({ channelId, filterId, onClose }: Props) {
    const { isLoading, error, data } = useGetChatFilter({
        channelId,
        filterId,
    })
    return (
        <Modal
            size="lg"
            opened={!!filterId}
            onClose={onClose}
            title={data ? `${data.name}` : 'Edit Filter'}
        >
            {isLoading && <PageLoader />}
            {error && <ErrorBox errorObj={error} />}
            {data && <EditFilter filter={data} onUpdated={() => onClose()} />}
        </Modal>
    )
}

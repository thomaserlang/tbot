import { ErrorBox } from '@/components/error-box'
import { PageLoader } from '@/components/page-loader'
import { ChatFilterId } from '@/features/channel-chat-filters/filter.types'
import { ChannelId } from '@/features/channel/types/channel.types'
import { Modal } from '@mantine/core'
import { useGetBannedTerm } from './banned-term.api'
import { BannedTerm, BannedTermId } from './banned-terms.types'
import { EditBannedTerm } from './edit-banned-term'

interface Props {
    channelId: ChannelId
    chatFilterId: ChatFilterId
    bannedTermId: BannedTermId
    onUpdated?: (bannedTerm: BannedTerm) => void
    onClose: () => void
}

export function EditBannedTermModal({
    channelId,
    chatFilterId,
    bannedTermId,
    onUpdated,
    onClose,
}: Props) {
    const { data, isLoading, error } = useGetBannedTerm({
        channelId,
        chatFilterId,
        bannedTermId,
    })

    return (
        <Modal opened={!!chatFilterId} onClose={onClose} title="Banned Term">
            {isLoading && <PageLoader />}
            {error && <ErrorBox errorObj={error} />}
            {data && (
                <EditBannedTerm
                    channelId={channelId}
                    bannedTerm={data}
                    onUpdated={(data) => {
                        onUpdated?.(data)
                        onClose()
                    }}
                />
            )}
        </Modal>
    )
}

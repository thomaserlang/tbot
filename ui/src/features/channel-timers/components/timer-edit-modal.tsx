import { ErrorBox } from '@/components/error-box'
import { PageLoader } from '@/components/page-loader'
import { ChannelId } from '@/features/channel'
import { Modal } from '@mantine/core'
import { useGetTimer } from '../timer.api'
import { TimerId } from '../timer.types'
import { EditTimerForm } from './timer-edit-form'

interface Props {
    channelId: ChannelId
    timerId: TimerId
    onClose: () => void
}

export function EditTimerModal({ channelId, timerId, onClose }: Props) {
    const { isLoading, error, data } = useGetTimer({
        channelId,
        timerId,
    })
    return (
        <Modal
            size="lg"
            opened={!!timerId}
            onClose={onClose}
            title="Edit Timer"
        >
            {isLoading && <PageLoader />}
            {error && <ErrorBox errorObj={error} />}
            {data && (
                <EditTimerForm
                    timer={data}
                    onUpdated={() => {
                        onClose()
                    }}
                />
            )}
        </Modal>
    )
}

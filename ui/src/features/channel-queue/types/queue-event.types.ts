import { QueueViewer } from './queue-viewer.types'

export interface QueueEvent {
    type:
        | 'channel_queue_viewer_created'
        | 'channel_queue_viewer_deleted'
        | 'channel_queue_viewer_moved'
        | 'channel_queue_cleared'
    channel_queue_viewer?: QueueViewer | null
}

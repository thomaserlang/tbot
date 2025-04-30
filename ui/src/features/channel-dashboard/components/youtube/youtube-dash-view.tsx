import { ChannelProviderDashComponentProps } from '../../types'
import { BroadcastScheduleButton } from './broadcast-schedule-button'

export function YoutubeDashView(props: ChannelProviderDashComponentProps) {
    return (
        <>
            <BroadcastScheduleButton channelProvider={props.channelProvider} />
        </>
    )
}

import { ChannelProviderDashComponentProps } from '../../types'
import { YoutubeCreateBroadcastButton } from './youtube-create-broadcast-button'

export function YoutubeDashView(props: ChannelProviderDashComponentProps) {
    return (
        <>
            <YoutubeCreateBroadcastButton
                channelProvider={props.channelProvider}
            />
        </>
    )
}

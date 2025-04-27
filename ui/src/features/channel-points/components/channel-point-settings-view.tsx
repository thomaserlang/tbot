import { ErrorBox } from '@/components/error-box'
import { PageLoader } from '@/components/page-loader'
import { ChannelId } from '@/features/channel'
import { Paper } from '@mantine/core'
import { useGetChannelPointSettings } from '../api/channel-point-settings.api'
import { ChannelPointSettingsForm } from './channel-point-settings-form'

interface Props {
    channelId: ChannelId
}

export function ChannelPointSettingsView({ channelId }: Props) {
    const { data, isLoading, error } = useGetChannelPointSettings({ channelId })

    if (isLoading || !data) return <PageLoader />
    if (error) return <ErrorBox errorObj={error} />

    return (
        <Paper withBorder p="1rem">
            <ChannelPointSettingsForm settings={data} />
        </Paper>
    )
}

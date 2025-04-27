import { ErrorBox } from '@/components/error-box'
import { PageLoader } from '@/components/page-loader'
import { ChannelId } from '@/features/channel'
import { Paper } from '@mantine/core'
import { useGetSlotsSettings } from '../api/slots-settings.api'
import { SlotsSettingsForm } from './slots-settings-form'

interface Props {
    channelId: ChannelId
}

export function SlotsSettingsView({ channelId }: Props) {
    const { data, isLoading, error } = useGetSlotsSettings({ channelId })

    if (isLoading || !data) return <PageLoader />
    if (error) return <ErrorBox errorObj={error} />

    return (
        <Paper withBorder p="1rem">
            <SlotsSettingsForm settings={data} />
        </Paper>
    )
}

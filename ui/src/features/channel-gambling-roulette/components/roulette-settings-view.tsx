import { ErrorBox } from '@/components/error-box'
import { PageLoader } from '@/components/page-loader'
import { ChannelId } from '@/features/channel'
import { Paper } from '@mantine/core'
import { useGetRouletteSettings } from '../api/roulette-settings.api'
import { RouletteSettingsForm } from './roulette-settings-form'

interface Props {
    channelId: ChannelId
}

export function RouletteSettingsView({ channelId }: Props) {
    const { data, isLoading, error } = useGetRouletteSettings({ channelId })

    if (isLoading || !data) return <PageLoader />
    if (error) return <ErrorBox errorObj={error} />

    return (
        <Paper withBorder p="1rem">
            <RouletteSettingsForm settings={data} />
        </Paper>
    )
}

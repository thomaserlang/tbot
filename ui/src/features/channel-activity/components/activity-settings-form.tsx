import { useCurrentUserSettings } from '@/components/current-user'
import { Flex, Switch } from '@mantine/core'

export function ActivitySettingsForm() {
    const { settings, updateSettings } = useCurrentUserSettings()
    return (
        <Flex gap="1rem" direction="column">
            <Switch
                label="Read indicator"
                checked={settings.activity_feed_read_indicator}
                onChange={(e) =>
                    updateSettings({
                        activity_feed_read_indicator: e.currentTarget.checked,
                    })
                }
            />
        </Flex>
    )
}

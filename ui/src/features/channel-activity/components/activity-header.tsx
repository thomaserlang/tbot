import { useCurrentUserSettings } from '@/components/current-user/current-user-settings.provider'
import { ActionIcon, Flex, Text } from '@mantine/core'
import {
    IconDotsVertical,
    IconFilter,
    IconFilterFilled,
} from '@tabler/icons-react'
import { ActivityFilters } from './activity-filters'
import { ActivityMenu } from './activity-menu'

export function ActivityFeedHeader() {
    const { settings } = useCurrentUserSettings()

    return (
        <Flex gap="1rem">
            <Text fw={500}>Activity Feed</Text>

            <Flex ml="auto" gap="0.5rem" align="center">
                <ActivityFilters>
                    <ActionIcon variant="subtle" size="compact-md" color="gray">
                        {settings.activity_feed_not_types.length > 0 ? (
                            <IconFilterFilled size={18} />
                        ) : (
                            <IconFilter size={18} />
                        )}
                    </ActionIcon>
                </ActivityFilters>

                <ActivityMenu>
                    <ActionIcon
                        variant="subtle"
                        size="compact-md"
                        color="gray"
                        mr="-0.25rem"
                    >
                        <IconDotsVertical size={18} />
                    </ActionIcon>
                </ActivityMenu>
            </Flex>
        </Flex>
    )
}

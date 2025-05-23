import { HoverCard, MantineSize, Text } from '@mantine/core'
import { useMemo } from 'react'
import { Activity } from '../types/activity.type'

interface Props {
    activity: Activity
    size?: MantineSize
}

export function ActivityMessage({ activity, size }: Props) {
    const a = useMemo(() => {
        return (
            <HoverCard width={500} shadow="md" position="bottom-start">
                <HoverCard.Target>
                    <Text size={size} c="dimmed">
                        {activity.message}
                    </Text>
                </HoverCard.Target>
                <HoverCard.Dropdown style={{ pointerEvents: 'none' }}>
                    <Text>{activity.message}</Text>
                </HoverCard.Dropdown>
            </HoverCard>
        )
    }, [`${activity.id}-message`])
    return a
}

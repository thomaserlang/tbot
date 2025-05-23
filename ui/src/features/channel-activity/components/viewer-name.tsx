import { Flex, MantineSize, Text } from '@mantine/core'
import { IconArrowRightBar } from '@tabler/icons-react'
import { Activity } from '../types/activity.type'

interface Props {
    activity: Activity
    size: MantineSize
}

export function ViewerName({ activity, size }: Props) {
    if (activity.gifted_viewers?.length == 1) {
        return (
            <Flex gap="0.25rem" align="center">
                <Text size={size} fw={500}>
                    {activity.viewer_display_name}
                </Text>
                <IconArrowRightBar />
                <Text size={size} fw={500}>
                    {activity.gifted_viewers[0].display_name}
                </Text>
            </Flex>
        )
    }

    return (
        <Text size={size} fw={500}>
            {activity.viewer_display_name}
        </Text>
    )
}

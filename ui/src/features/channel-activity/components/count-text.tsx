import { Flex, MantineSize, Text } from '@mantine/core'
import { IconList } from '@tabler/icons-react'
import { Activity } from '../types/activity.type'
import { GiftedViewersList } from './gifted-viewers-list'

interface Props {
    activity: Activity
    size: MantineSize
}

export function CountText({ activity, size }: Props) {
    if (activity.count_currency) {
        const countValue =
            activity.count / Math.pow(10, activity.count_decimal_place)
        return (
            <Text fz={size} fw={500}>
                {(isNaN(countValue) ? 0 : countValue).toLocaleString(
                    undefined,
                    {
                        minimumFractionDigits: 0,
                        maximumFractionDigits: 2,
                        style: 'currency',
                        currency: activity.count_currency,
                    }
                )}
            </Text>
        )
    }

    if (activity.count_name == 'months') {
        return (
            <Text fz={size} fw={500}>
                {activity.count}mo
            </Text>
        )
    }

    if (activity.gifted_viewers && activity.gifted_viewers?.length > 1) {
        return (
            <GiftedViewersList activity={activity}>
                <Flex
                    style={{ cursor: 'pointer' }}
                    gap="0.25rem"
                    align="center"
                    onClick={(e) => {
                        e.stopPropagation()
                    }}
                >
                    <Text fz={size} fw={500}>
                        {activity.count}
                    </Text>{' '}
                    <IconList size={14} />
                </Flex>
            </GiftedViewersList>
        )
    }

    return (
        <Text fz={size} fw={500}>
            {activity.count.toLocaleString()} {activity.count_name}
        </Text>
    )
}

import { providerInfo } from '@/constants'
import { Badge, Box, Flex, MantineSize } from '@mantine/core'
import { Activity } from '../types/activity.type'
import { CountText } from './count-text'
import { ViewerName } from './viewer-name'

interface Props {
    activity: Activity
    size?: MantineSize
}

export function InfoColumn({ activity, size = 'sm' }: Props) {
    return (
        <Flex gap="0.35rem" align="center">
            <Box
                style={{
                    position: 'relative',
                    top: '0.15rem',
                }}
                c={providerInfo[activity.provider].color}
            >
                {providerInfo[activity.provider].icon?.({ size: 18 })}
            </Box>

            <Badge
                radius="xs"
                autoContrast
                color={activity.color}
                fw={500}
                fz={size}
                tt="none"
                style={{ display: 'inline' }}
                title={activity.type_display_name}
                pl="0.35rem"
                pr="0.35rem"
            >
                {activity.type_display_name}
            </Badge>

            <Box ml="0.5rem" mr="0.5rem">
                <ViewerName activity={activity} size={size} />
            </Box>

            {!!activity.count && (
                <Badge
                    radius="xs"
                    autoContrast
                    color="gray"
                    fw={500}
                    fz={size}
                    tt="none"
                    style={{ display: 'flex' }}
                    title={activity.count_name}
                    pl="0.35rem"
                    pr="0.35rem"
                >
                    <CountText activity={activity} size={size} />
                </Badge>
            )}

            {activity.sub_type_display_name && (
                <Badge
                    radius="xs"
                    autoContrast
                    color="gray"
                    fw={500}
                    fz={size}
                    tt="none"
                    style={{ display: 'flex' }}
                    maw={'5rem'}
                    title={activity.sub_type_display_name}
                    pl="0.35rem"
                    pr="0.35rem"
                >
                    {activity.sub_type_display_name}
                </Badge>
            )}
        </Flex>
    )
}

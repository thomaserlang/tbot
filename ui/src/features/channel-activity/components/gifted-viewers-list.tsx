import { Box, Popover, SimpleGrid } from '@mantine/core'
import { Activity } from '../types/activity.type'

interface Props {
    children: React.ReactElement
    activity: Activity
}

export function GiftedViewersList({ activity, children }: Props) {
    if (!activity.gifted_viewers) return
    if (activity.gifted_viewers.length <= 1) return

    return (
        <Popover position="bottom" withArrow shadow="md">
            <Popover.Target>{children}</Popover.Target>
            <Popover.Dropdown>
                <SimpleGrid
                    cols={{
                        base: 2,
                        md: 3,
                        lg: 4,
                    }}
                    spacing="xs"
                    p="0.5rem"
                    style={{ maxHeight: '300px', overflowY: 'auto' }}
                >
                    <>
                        {activity.gifted_viewers?.map((viewer, index) => (
                            <Box key={index}>
                                {index + 1}. {viewer.display_name}
                            </Box>
                        ))}
                    </>
                </SimpleGrid>
            </Popover.Dropdown>
        </Popover>
    )
}

import { Flex, MantineFontSize, Text } from '@mantine/core'
import { IconUserFilled } from '@tabler/icons-react'

interface Props {
    count: number | null
    size?: MantineFontSize
    iconSize?: string | number
}

export function ViewerCount({ count, size = 'sm', iconSize = 14 }: Props) {
    if (count === null) return
    return (
        <Flex align="center" gap="0.10rem" title="Concurrent viewers" c="red">
            <Text size={size}>{count.toLocaleString()}</Text>
            <IconUserFilled size={iconSize} />
        </Flex>
    )
}

import { Anchor, Box, Flex, Image, StyleProp } from '@mantine/core'

interface Props {
    width: StyleProp<React.CSSProperties['width']>
}
export function Logo({ width }: Props) {
    return (
        <Flex gap="0.5rem" align="center">
            <Box style={{ width: '13%', height: '13%' }}>
                <Anchor href="/channels">
                    <Image src="/tree.svg" alt="Synchra" />
                </Anchor>
            </Box>
            <Anchor href="/channels">
                <Image src="/logo.svg" alt="Synchra" w={width} />
            </Anchor>
        </Flex>
    )
}

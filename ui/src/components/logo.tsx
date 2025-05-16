import { Anchor, Box, Flex, Image, StyleProp } from '@mantine/core'
import logoUrl from './logo.svg'
import treeUrl from './treeOutline.svg'

interface Props {
    width: StyleProp<React.CSSProperties['width']>
}
export function Logo({ width }: Props) {
    return (
        <Flex gap="0.5rem" align="center">
            <Box>
                <Anchor href="/channels">
                    <Image src={treeUrl} alt="Synchra" h={40} />
                </Anchor>
            </Box>
            <Anchor href="/channels">
                <Image src={logoUrl} alt="Synchra" w={width} />
            </Anchor>
        </Flex>
    )
}

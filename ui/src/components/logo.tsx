import { Anchor, Box, Flex, Image, Text } from '@mantine/core'
import treeUrl from './tree-outline.svg'

export function Logo() {
    return (
        <Flex gap="0.5rem" align="center">
            <Box>
                <Anchor href="/channels">
                    <Image src={treeUrl} alt="Synchra" w={53} h={40} />
                </Anchor>
            </Box>
            <Text fz={24} fw={500} component="a" href="/channels">
                Synchra
            </Text>
        </Flex>
    )
}

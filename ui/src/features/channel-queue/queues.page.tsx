import { Flex } from '@mantine/core'
import { useCurrentChannel } from '../channel'
import { SelectQueue } from './components/select-queue'

export function Component() {
    const channel = useCurrentChannel()
    return (
        <Flex>
            <SelectQueue channelId={channel.id} />
        </Flex>
    )
}

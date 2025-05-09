import { CommandCreate, CommandCreateModal } from '@/features/channel-commands'
import { ChannelId } from '@/features/channel/types/channel.types'
import { Button, Menu } from '@mantine/core'
import { IconChevronDown } from '@tabler/icons-react'
import { useState } from 'react'
import { useGetQueue } from '../api/queue.api'
import { ChannelQueueId } from '../types/queue.types'

interface Props {
    channelId: ChannelId
    queueId: ChannelQueueId
}

export function QueueCreateCommandButton({ channelId, queueId }: Props) {
    const [values, setValues] = useState<CommandCreate | null>(null)
    const queue = useGetQueue({
        channelId,
        queueId: queueId,
    })

    return (
        <>
            {values && (
                <CommandCreateModal
                    channelId={channelId}
                    opened={true}
                    onClose={() => setValues(null)}
                    initialValues={values}
                />
            )}

            <Menu shadow="md" width={200}>
                <Menu.Target>
                    <Button
                        variant="light"
                        rightSection={<IconChevronDown size={14} />}
                    >
                        Create Command
                    </Button>
                </Menu.Target>
                <Menu.Dropdown>
                    <Menu.Item
                        onClick={() => {
                            setValues({
                                response: `You have joined the queue as number: {queue_join.position ${queue.data?.name}}`,
                            })
                        }}
                    >
                        Join command
                    </Menu.Item>
                    <Menu.Item
                        onClick={() => {
                            setValues({
                                response: `You have left the queue {queue.leave ${queue.data?.name}}`,
                            })
                        }}
                    >
                        Leave command
                    </Menu.Item>
                    <Menu.Item
                        onClick={() => {
                            setValues({
                                response: `You are in position {queue.position ${queue.data?.name}}`,
                            })
                        }}
                    >
                        Position command
                    </Menu.Item>
                </Menu.Dropdown>
            </Menu>
        </>
    )
}

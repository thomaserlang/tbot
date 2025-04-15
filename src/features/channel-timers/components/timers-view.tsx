import { ErrorBox } from '@/components/error-box'
import { PageLoader } from '@/components/page-loader'
import { toastPromise } from '@/utils/toast'
import { Box, Button, Flex, Paper, Switch, Text } from '@mantine/core'
import { IconClock } from '@tabler/icons-react'
import { UseQueryResult } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { useUpdateTimer } from '../timer.api'
import { Timer } from '../timer.types'
import { TimerMenu } from './timer-menu'

interface Props {
    data: UseQueryResult<Timer[]>
    onEditClick?: (command: Timer) => void
}

export function TimersView({ data, onEditClick }: Props) {
    const navigate = useNavigate()

    if (data.isLoading) {
        return <PageLoader />
    }

    if (data.error) {
        return <ErrorBox errorObj={data.error} />
    }

    if (!data.data || data.data.length === 0) {
        return (
            <Flex justify="center" align="center" direction="column" gap="1rem">
                <IconClock size={80} />
                <Text size="xl" fw={500}>
                    No timers found, create one.
                </Text>
            </Flex>
        )
    }

    return (
        <Flex wrap={'wrap'} gap="1rem">
            {data.data.map((timer) => (
                <Paper key={timer.id} withBorder p="0.5rem" w="20rem">
                    <Flex gap="0.5rem" direction="column">
                        <Flex>
                            <Text fw={500}>{timer.name}</Text>
                            <Box ml="auto">
                                <TimerMenu
                                    timer={timer}
                                    onEditClick={onEditClick}
                                />
                            </Box>
                        </Flex>
                        <Flex gap="0.5rem" align="center">
                            <EnableFilterSwitch timer={timer} />

                            <Flex c="dimmed" gap="0.25rem" align="center">
                                <IconClock size={16} />
                                <Text size="sm"> {timer.interval} min</Text>
                            </Flex>

                            <Button
                                ml="auto"
                                size="xs"
                                variant="outline"
                                onClick={() => {
                                    navigate(
                                        `/channels/${timer.channel_id}/timers/${timer.id}`
                                    )
                                }}
                            >
                                Edit
                            </Button>
                        </Flex>
                    </Flex>
                </Paper>
            ))}
        </Flex>
    )
}

function EnableFilterSwitch({ timer }: { timer: Timer }) {
    const update = useUpdateTimer()
    return (
        <Switch
            onLabel={'On'}
            offLabel={'Off'}
            size="md"
            checked={timer.enabled}
            onChange={(e) => {
                toastPromise({
                    promise: update.mutateAsync({
                        channelId: timer.channel_id,
                        timerId: timer.id,
                        data: {
                            enabled: e.currentTarget.checked,
                        },
                    }),
                    loading: {
                        title: `${
                            e.currentTarget.checked ? 'Enabling' : 'Disabling'
                        } ${timer.name}...`,
                    },
                    success: {
                        title: `${timer.name} ${
                            e.currentTarget.checked ? 'enabled' : 'disabled'
                        }`,
                    },
                    error: {
                        title: 'Failed',
                    },
                })
            }}
        />
    )
}

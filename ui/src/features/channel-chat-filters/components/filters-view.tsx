import { ErrorBox } from '@/components/error-box'
import { PageLoader } from '@/components/page-loader'
import { ChannelId } from '@/features/channel/types'
import { toastPromise } from '@/utils/toast'
import { Box, Button, Flex, Paper, Switch, Text } from '@mantine/core'
import { IconShieldCog } from '@tabler/icons-react'
import { useNavigate } from 'react-router-dom'
import { ChatFilter } from '../filter-registry'
import { useUpdateChatFilter } from '../filter.api'
import { useGetChatFilters } from '../filters.api'
import { FilterMenu } from './filter-menu'

interface Props {
    channelId: ChannelId
}

export function FiltersView({ channelId }: Props) {
    const { data, isLoading, error } = useGetChatFilters({
        channelId,
    })
    const navigate = useNavigate()

    if (isLoading) {
        return <PageLoader />
    }

    if (error) {
        return <ErrorBox errorObj={error} />
    }

    if (!data || data.length === 0) {
        return (
            <Flex justify="center" align="center" direction="column" gap="1rem">
                <IconShieldCog size={80} />
                <Text size="xl" fw={500}>
                    No chat filters found, add one.
                </Text>
            </Flex>
        )
    }

    return (
        <Flex wrap={'wrap'} gap="1rem">
            {data?.map((filter) => (
                <Paper key={filter.id} withBorder p="0.5rem" w="20rem">
                    <Flex gap="0.5rem" direction="column">
                        <Flex>
                            <Text fw={500}>{filter.name}</Text>
                            <Box ml="auto">
                                <FilterMenu filter={filter} />
                            </Box>
                        </Flex>
                        <Flex gap="0.5rem" align="center">
                            <EnableFilterSwitch filter={filter} />

                            <Button
                                ml="auto"
                                size="xs"
                                variant="outline"
                                onClick={() => {
                                    navigate(
                                        `/channels/${filter.channel_id}/chat-filters/${filter.id}`
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

function EnableFilterSwitch({ filter }: { filter: ChatFilter }) {
    const update = useUpdateChatFilter()
    return (
        <Switch
            onLabel={'On'}
            offLabel={'Off'}
            size="md"
            checked={filter.enabled}
            onChange={(e) => {
                toastPromise({
                    promise: update.mutateAsync({
                        channelId: filter.channel_id,
                        filterId: filter.id,
                        data: {
                            type: filter.type,
                            enabled: e.currentTarget.checked,
                        },
                    }),
                    loading: {
                        title: `${
                            e.currentTarget.checked ? 'Enabling' : 'Disabling'
                        } ${filter.name}...`,
                    },
                    success: {
                        title: `${filter.name} ${
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

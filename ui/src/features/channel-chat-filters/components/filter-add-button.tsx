import { ChannelId } from '@/features/channel'
import { toastError } from '@/utils/toast'
import { Button, Menu } from '@mantine/core'
import { IconPlus } from '@tabler/icons-react'
import { ChatFilter, registeredFilters } from '../filter-registry'
import { useCreateChatFilter } from '../filter.api'

interface Props {
    channelId: ChannelId
    onCreated?: (filter: ChatFilter) => void
}

export function AddFilterButton({ channelId, onCreated }: Props) {
    const add = useCreateChatFilter({
        onSuccess: (data) => {
            onCreated?.(data)
        },
        onError: (error) => {
            toastError(error)
        },
    })
    return (
        <Menu width={200}>
            <Menu.Target>
                <Button
                    ml="auto"
                    variant="light"
                    loading={add.isPending}
                    leftSection={<IconPlus size={14} />}
                >
                    Add Filter
                </Button>
            </Menu.Target>

            <Menu.Dropdown>
                {Object.values(registeredFilters).map((filterType) => (
                    <Menu.Item
                        key={filterType.type}
                        onClick={() => {
                            add.mutate({
                                channelId,
                                data: {
                                    type: filterType.type,
                                },
                            })
                        }}
                    >
                        {filterType.name}
                    </Menu.Item>
                ))}
            </Menu.Dropdown>
        </Menu>
    )
}

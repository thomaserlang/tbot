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

export function CreateFilterButton({ channelId, onCreated }: Props) {
    const create = useCreateChatFilter({
        onSuccess: (data) => {
            onCreated?.(data)
        },
        onError: (error) => {
            toastError(error)
        },
    })
    return (
        <>
            <Menu>
                <Menu.Target>
                    <Button
                        ml="auto"
                        variant="light"
                        loading={create.isPending}
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
                                create.mutate({
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
        </>
    )
}

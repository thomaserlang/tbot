import { Container, Flex, Title } from '@mantine/core'
import { useNavigate, useParams } from 'react-router-dom'
import { useCurrentChannel } from '../channel/current-channel.provider'
import { AddFilterButton } from './components/filter-add-button'
import { EditFilterModal } from './components/filter-edit-modal'
import { FiltersView } from './components/filters-view'
import { ChatFilterId } from './filter.types'

export function Component() {
    const channel = useCurrentChannel()
    const { filterId } = useParams<{ filterId?: ChatFilterId }>()
    const navigate = useNavigate()

    return (
        <>
            <Container size="xl">
                <Flex
                    direction="column"
                    gap="1rem"
                    h="var(--tbot-content-height)"
                >
                    <Flex>
                        <Title order={2}>Chat Filters</Title>

                        <AddFilterButton
                            channelId={channel.id}
                            onCreated={(filter) => {
                                navigate(
                                    `/channels/${channel.id}/chat-filters/${filter.id}`
                                )
                            }}
                        />
                    </Flex>

                    <FiltersView channelId={channel.id} />
                </Flex>
            </Container>

            {filterId && (
                <EditFilterModal
                    channelId={channel.id}
                    filterId={filterId}
                    onClose={() => {
                        navigate(`/channels/${channel.id}/chat-filters`)
                    }}
                />
            )}
        </>
    )
}

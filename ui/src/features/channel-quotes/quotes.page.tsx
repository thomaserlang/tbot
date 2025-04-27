import { Container, Flex, Title } from '@mantine/core'
import { useNavigate, useParams } from 'react-router-dom'
import { useCurrentChannel } from '../channel'
import { CreateQuoteButton } from './components/quote-create-button'
import { EditQuoteModal } from './components/quote-edit-modal'
import { QuotesTable } from './components/quotes-table'
import { ChannelQuoteId } from './types/quote.types'

export function Component() {
    const channel = useCurrentChannel()
    const { channelQuoteId } = useParams<{ channelQuoteId?: ChannelQuoteId }>()
    const navigate = useNavigate()

    return (
        <>
            <Container size="lg">
                <title>Quotes</title>
                <Flex
                    h="var(--tbot-content-height)"
                    direction="column"
                    gap="1rem"
                >
                    <Flex>
                        <Title order={2}>Quotes</Title>

                        <CreateQuoteButton channelId={channel.id} />
                    </Flex>

                    <QuotesTable
                        channelId={channel.id}
                        onEditClick={(quote) => {
                            navigate(quote.id)
                        }}
                    />
                </Flex>
            </Container>

            {channelQuoteId && (
                <EditQuoteModal
                    channelId={channel.id}
                    channelQuoteId={channelQuoteId}
                    onClose={() => {
                        navigate(`/channels/${channel.id}/quotes`)
                    }}
                />
            )}
        </>
    )
}

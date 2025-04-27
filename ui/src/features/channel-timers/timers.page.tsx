import { ErrorBox } from '@/components/error-box'
import { useCurrentChannel } from '@/features/channel'
import { useDocumentTitle } from '@/utils/document-title'
import { Container, Flex, Title } from '@mantine/core'
import { useNavigate, useParams } from 'react-router-dom'
import { CreatetimerButton } from './components/timer-create-button'
import { EditTimerModal } from './components/timer-edit-modal'
import { TimersView } from './components/timers-view'
import { TimerId } from './timer.types'
import { useGetTimers } from './timers.api'

export function Component() {
    const channel = useCurrentChannel()
    const data = useGetTimers(channel.id)
    const { timerId } = useParams<{ timerId?: TimerId }>()
    const navigate = useNavigate()

    useDocumentTitle(`Channel Timers - ${channel.display_name}`)

    return (
        <>
            <Container size="xl">
                <Flex
                    direction="column"
                    gap="1rem"
                    h="var(--tbot-content-height)"
                >
                    <Flex>
                        <Title order={2}>Timers</Title>

                        <CreatetimerButton
                            channelId={channel.id}
                            onCreated={() => {
                                data.refetch()
                            }}
                        />
                    </Flex>
                    {data.error && <ErrorBox errorObj={data.error} />}
                    {!data.error && (
                        <TimersView
                            data={data}
                            onEditClick={(timer) => navigate(timer.id)}
                        />
                    )}
                </Flex>
            </Container>
            {timerId && (
                <EditTimerModal
                    channelId={channel.id}
                    timerId={timerId}
                    onClose={() => {
                        navigate(`/channels/${channel.id}/timers`)
                    }}
                />
            )}
        </>
    )
}

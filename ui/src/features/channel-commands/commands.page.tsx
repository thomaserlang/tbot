import { ErrorBox } from '@/components/error-box'
import { useCurrentChannel } from '@/features/channel'
import { useDocumentTitle } from '@/utils/document-title'
import { Container, Flex, Title } from '@mantine/core'
import { useNavigate, useParams } from 'react-router-dom'
import { useGetCommands } from './api/commands.api'
import { CommandCreateButton } from './components/command-create-button'
import { CommandEditModal } from './components/command-edit-modal'
import { CommandsTable } from './components/commands-table'
import { CommandId } from './types/command.types'

export function Component() {
    const channel = useCurrentChannel()
    const data = useGetCommands(channel.id)
    const { commandId } = useParams<{ commandId?: CommandId }>()
    const navigate = useNavigate()

    useDocumentTitle(`Channel Commands - ${channel.display_name}`)

    return (
        <>
            <Container size="xl">
                <Flex
                    direction="column"
                    gap="1rem"
                    h="var(--tbot-content-height)"
                >
                    <Flex>
                        <Title order={2}>Commands</Title>

                        <CommandCreateButton
                            channelId={channel.id}
                            onCreated={() => {
                                data.refetch()
                            }}
                        />
                    </Flex>
                    {data.error && <ErrorBox errorObj={data.error} />}
                    {!data.error && (
                        <CommandsTable
                            data={data}
                            onEditClick={(command) => navigate(command.id)}
                        />
                    )}
                </Flex>
            </Container>

            {commandId && (
                <CommandEditModal
                    channelId={channel.id}
                    commandId={commandId}
                    onClose={() => {
                        navigate(`/channels/${channel.id}/commands`)
                    }}
                />
            )}
        </>
    )
}

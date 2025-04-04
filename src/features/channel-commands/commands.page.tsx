import { useCurrentChannel } from '@/features/channel'
import { Container, Flex, Modal, Title } from '@mantine/core'
import { useNavigate, useParams } from 'react-router-dom'
import { useGetCommands } from './commands.api'
import { CommandId } from './commands.types'
import { EditCommandModal } from './components/command-edit-modal'
import { CreateCommandButton } from './components/commands-create-button'
import { CommandsTable } from './components/commands-table'

export function Component() {
    const channel = useCurrentChannel()
    const data = useGetCommands(channel.id)
    const { commandId } = useParams<{ commandId?: CommandId }>()
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
                        <Title order={2}>Commands</Title>

                        <CreateCommandButton
                            channelId={channel.id}
                            onCreated={() => {
                                data.refetch()
                            }}
                        />
                    </Flex>
                    <CommandsTable
                        data={data}
                        onEditClick={(command) => navigate(command.id)}
                    />
                </Flex>
            </Container>
            {
                <Modal
                    opened={!!commandId}
                    onClose={() => {}}
                    title="Edit Command"
                >
                    {commandId && (
                        <EditCommandModal
                            channelId={channel.id}
                            commandId={commandId}
                            onClose={() => {
                                navigate(`/channels/${channel.id}/commands`)
                            }}
                        />
                    )}
                </Modal>
            }
        </>
    )
}

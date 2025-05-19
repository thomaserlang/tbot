import { ErrorBox } from '@/components/error-box'
import { useCurrentChannel } from '@/features/channel'
import { useDocumentTitle } from '@/utils/document-title'
import { Button, Container, Flex, Title } from '@mantine/core'
import { IconListCheck, IconPlus } from '@tabler/icons-react'
import { useNavigate, useParams } from 'react-router-dom'
import { CommandTemplateImport } from './command-template/components/command-template-import'
import { useGetCommands } from './command/api/commands.api'
import { CommandCreate } from './command/components/command-create'
import { CommandEditModal } from './command/components/command-edit-modal'
import { CommandsTable } from './command/components/commands-table'
import { CommandId } from './command/types/command.types'

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
                    <Flex justify="space-between">
                        <Title order={2}>Commands</Title>

                        <Flex gap="1rem">
                            <CommandTemplateImport>
                                <Button
                                    ml="auto"
                                    variant="light"
                                    leftSection={<IconListCheck size={16} />}
                                >
                                    Command Templates
                                </Button>
                            </CommandTemplateImport>

                            <CommandCreate
                                channelId={channel.id}
                                onCreated={() => {
                                    data.refetch()
                                }}
                            >
                                <Button
                                    ml="auto"
                                    variant="light"
                                    leftSection={<IconPlus size={16} />}
                                >
                                    Create Command
                                </Button>
                            </CommandCreate>
                        </Flex>
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

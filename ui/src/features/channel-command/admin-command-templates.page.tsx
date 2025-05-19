import { Container, Flex } from '@mantine/core'
import { useNavigate, useParams } from 'react-router-dom'
import { CommandTemplateEditModal } from './command-template/components/command-template-edit-modal'
import { CommandTemplatesAdminView } from './command-template/components/command-templates-admin-view'
import { CommandTemplateId } from './command-template/types/command-template.types'

export function Component() {
    const { commandTemplateId } = useParams<{
        commandTemplateId?: CommandTemplateId
    }>()
    const navigate = useNavigate()

    return (
        <>
            <title>Admin Command Templates</title>

            {commandTemplateId && (
                <CommandTemplateEditModal
                    opened={!!commandTemplateId}
                    commandTemplateId={commandTemplateId}
                    onClose={() => {
                        navigate('/admin/command-templates')
                    }}
                />
            )}
            <Container size="xl">
                <Flex
                    direction="column"
                    gap="1rem"
                    h="var(--tbot-content-height)"
                >
                    <CommandTemplatesAdminView
                        onEditClick={(commandTemplate) => {
                            navigate(
                                `/admin/command-templates/${commandTemplate.id}`
                            )
                        }}
                    />
                </Flex>
            </Container>
        </>
    )
}

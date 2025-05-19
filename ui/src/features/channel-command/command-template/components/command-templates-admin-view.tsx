import { Flex, Title } from '@mantine/core'
import { CommandTemplate } from '../types/command-template.types'
import { CommandTemplateCreateButton } from './command-template-create-button'
import { CommandTemplatesTable } from './command-templates-table'

interface Props {
    onEditClick?: (commandTemplate: CommandTemplate) => void
}

export function CommandTemplatesAdminView({ onEditClick }: Props) {
    return (
        <>
            <Flex justify="space-between" align="center">
                <Title order={2}>Command Templates</Title>

                <CommandTemplateCreateButton />
            </Flex>

            <CommandTemplatesTable onEditClick={onEditClick} />
        </>
    )
}

import { ErrorBox } from '@/components/error-box'
import { PageLoader } from '@/components/page-loader'
import { Modal } from '@mantine/core'
import { useGetCommandTemplate } from '../api/command-template.api'
import {
    CommandTemplate,
    CommandTemplateId,
} from '../types/command-template.types'
import { CommandTemplateEditForm } from './command-template-edit-form'

interface Props {
    commandTemplateId: CommandTemplateId
    opened: boolean
    onClose: () => void
    onCreated?: (template: CommandTemplate) => void
}

export function CommandTemplateEditModal({
    commandTemplateId,
    opened,
    onClose,
    onCreated,
}: Props) {
    const { data, isLoading, error } = useGetCommandTemplate({
        commandTemplateId,
    })

    if (isLoading) return <PageLoader />
    if (error) return <ErrorBox errorObj={error} />

    return (
        <Modal
            opened={opened}
            onClose={onClose}
            title="Edit command template"
            size="lg"
        >
            {opened && data && (
                <CommandTemplateEditForm
                    commandTemplate={data}
                    onUpdated={(template) => {
                        onCreated?.(template)
                        onClose()
                    }}
                />
            )}
        </Modal>
    )
}

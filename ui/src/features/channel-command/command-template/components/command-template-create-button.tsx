import { Button } from '@mantine/core'
import { useDisclosure } from '@mantine/hooks'
import { IconPlus } from '@tabler/icons-react'
import { CommandTemplateCreateModal } from './command-template-create-modal'

interface Props {}

export function CommandTemplateCreateButton({}: Props) {
    const [opened, { open, close }] = useDisclosure(false)

    return (
        <>
            <Button
                variant="light"
                leftSection={<IconPlus size={16} />}
                onClick={open}
            >
                Create command template
            </Button>

            <CommandTemplateCreateModal opened={opened} onClose={close} />
        </>
    )
}

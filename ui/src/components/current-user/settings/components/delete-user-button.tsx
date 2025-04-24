import { Button, Modal } from '@mantine/core'
import { useDisclosure } from '@mantine/hooks'
import { DeleteUserConfirm } from './delete-user-confirm'

export function DeleteUserButton() {
    const [opened, { open, close }] = useDisclosure(false)

    return (
        <>
            <Button variant="outline" color="red" onClick={open}>
                Delete user profile
            </Button>

            <Modal title="Delete user profile" opened={opened} onClose={close}>
                {opened && <DeleteUserConfirm />}
            </Modal>
        </>
    )
}

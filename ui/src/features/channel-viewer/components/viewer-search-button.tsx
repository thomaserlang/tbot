import { Button, Modal } from '@mantine/core'
import { useDisclosure } from '@mantine/hooks'
import { IconSearch } from '@tabler/icons-react'
import { ViewerName } from '../types/viewer.type'
import { ViewerSearch } from './viewer-search'

interface Props {
    onSelect: (chatter: ViewerName) => void
}

export function ViewerSearchButton({ onSelect }: Props) {
    const [opened, { open, close }] = useDisclosure(false)
    return (
        <>
            <Button
                onClick={open}
                variant="default"
                leftSection={<IconSearch size={14} />}
            >
                Viewer
            </Button>

            <Modal
                opened={opened}
                onClose={close}
                title="Search Viewer"
                size="md"
            >
                {opened && (
                    <ViewerSearch
                        onSelect={(chatter) => {
                            onSelect(chatter)
                            close()
                        }}
                    />
                )}
            </Modal>
        </>
    )
}

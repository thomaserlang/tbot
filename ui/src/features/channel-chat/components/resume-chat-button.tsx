import { Box, Button } from '@mantine/core'

interface Props {
    onClick: () => void
}

export function ResumeChatButton({ onClick }: Props) {
    return (
        <Box
            style={{
                position: 'relative',
            }}
        >
            <Button
                onClick={onClick}
                style={{
                    position: 'absolute',
                    bottom: '0.25rem',
                    left: '44%',
                }}
                variant="outline"
                color="blue"
            >
                Resume chat
            </Button>
        </Box>
    )
}

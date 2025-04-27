import { Button } from '@mantine/core'

interface Props {
    onClick: () => void
}

export function LoadMoreButton({ onClick }: Props) {
    return (
        <Button
            onClick={onClick}
            variant="outline"
            color="blue"
            style={{
                margin: '10px auto',
                display: 'block',
                width: 'fit-content',
            }}
        >
            Load more
        </Button>
    )
}

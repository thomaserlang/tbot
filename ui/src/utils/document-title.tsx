import { APP_TITLE } from '@/constants'
import { useIsomorphicEffect } from '@mantine/hooks'

function setDocumentTitle(title: string) {
    document.title = `${title} | ${APP_TITLE}`
}

export function useDocumentTitle(title: string) {
    useIsomorphicEffect(() => {
        const prevTitle = document.title

        setDocumentTitle(title)

        return () => {
            document.title = prevTitle
        }
    }, [title])
}

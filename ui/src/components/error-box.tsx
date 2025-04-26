import { Alert } from '@mantine/core'
import { IconAlertCircle } from '@tabler/icons-react'
import { AxiosError } from 'axios'
import { ReactNode } from 'react'

interface Props {
    message?: string
    errorObj?: AxiosError | string | unknown
}

export function ErrorBox({ message, errorObj }: Props) {
    return (
        <Alert title="Error" color="red" icon={<IconAlertCircle size={14} />}>
            {message || errorMessageFromResponse(errorObj)}
        </Alert>
    )
}

export function errorMessageFromResponse(errorObj: any): ReactNode {
    if (!errorObj) return <>Unknown error</>

    if (typeof errorObj === 'string') return <>{errorObj}</>

    if (errorObj.isAxiosError) {
        const error: AxiosError = errorObj

        const data = error.response?.data as any
        if (error.status === 422) {
            for (const e of data.detail) {
                if (e.loc.length > 1) {
                    return (
                        <>
                            {e.msg.replace('String', '')} {e.loc[1]}
                        </>
                    )
                }
            }
        }
        if (data?.detail) return <>{data?.detail}</>

        return <>{error.message}</>
    }
    return <>{errorObj.detail}</>
}

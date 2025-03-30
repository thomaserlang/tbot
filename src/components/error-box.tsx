import { Alert } from '@mantine/core'
import { IconAlertCircle } from '@tabler/icons-react'
import { AxiosError } from 'axios'
import { ReactNode } from 'react'

interface IProps {
    message?: string
    errorObj?: AxiosError | string | unknown
}

export function ErrorBox({ message, errorObj }: IProps) {
    return (
        <Alert title="Fejl" color="red" icon={<IconAlertCircle size={14} />}>
            {message || errorMessageFromResponse(errorObj)}
        </Alert>
    )
}

export function errorMessageFromResponse(errorObj: any): ReactNode {
    if (!errorObj) return <>'Unknown error'</>

    if (typeof errorObj === 'string') return <>{errorObj}</>

    if (errorObj.isAxiosError) {
        const e: AxiosError = errorObj
        const data = e.response?.data as any
        if (data?.code == 1001) {
            return (
                <>
                    {data.errors.length > 0 && (
                        <>
                            <b>{data.message}</b>
                            <ul>
                                {data.errors.map((error: any, index: any) => (
                                    <li key={index}>
                                        {error['field'].join('.')}:{' '}
                                        {error['message']}
                                    </li>
                                ))}
                            </ul>
                        </>
                    )}
                </>
            )
        }
        if (data?.message) return <>{data?.message}</>

        return <>{e.message}</>
    }
    return <>{errorObj.message}</>
}

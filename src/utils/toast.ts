import { errorMessageFromResponse } from '@/components/error-box'
import { notifications } from '@mantine/notifications'

export function toastSuccess(message: string) {
    notifications.show({
        title: message,
        message: '',
        color: 'green',
        autoClose: 2000,
        withBorder: true,
    })
}

export function toastError(errorObj: any) {
    notifications.show({
        title: 'Error',
        message: errorMessageFromResponse(errorObj),
        color: 'red',
        autoClose: 20000,
        withBorder: true,
    })
}

export async function toastPromise({
    promise,
    loading,
    success,
    error,
}: {
    promise: Promise<any>
    loading: {
        title?: string
        message?: string
    }
    success: {
        title?: string
        message?: string
        onSuccess?: () => void
    }
    error?: {
        title?: string
        message?: string
        onError?: () => void
    }
}) {
    const id = notifications.show({
        loading: true,
        title: loading.title,
        message: loading.message,
        autoClose: false,
        withBorder: true,
    })
    try {
        await promise
        notifications.update({
            id,
            loading: false,
            title: success.title,
            message: success.message,
            color: 'green',
            autoClose: 1500,
        })
        success.onSuccess?.()
    } catch (e) {
        notifications.update({
            id,
            loading: false,
            title: error?.title || 'Fejl',
            message: error?.message || errorMessageFromResponse(e),
            color: 'red',
            autoClose: 10000,
        })
        error?.onError?.()
    }
}

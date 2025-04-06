import { PageCursor } from '@/types/page-cursor.type'
import axios, { AxiosError, AxiosRequestConfig } from 'axios'

export const api = axios.create({
    paramsSerializer: {
        indexes: null,
    },
})
api.interceptors.response.use(
    (response) => response,
    async (error: AxiosError) => {
        if (error?.response?.status == 401) {
            location.href = `/sign-in?next=${encodeURIComponent(
                location.pathname + location.search
            )}`
        }
        throw error
    }
)

export function setAuthorizationHeader() {
    if (localStorage.getItem('accessToken'))
        api.defaults.headers['Authorization'] = `Bearer ${localStorage.getItem(
            'accessToken'
        )}`
    else api.defaults.headers['Authorization'] = null
}
setAuthorizationHeader()

export function setAccessToken(token: string) {
    localStorage.setItem('accessToken', token)
    setAuthorizationHeader()
}

export async function getAllPagesCursor<T = any, D = any>(
    url: string,
    config: AxiosRequestConfig<D> = {}
) {
    let result = await api.get<PageCursor<T>>(url, config)
    if (!config.params) config.params = {}
    const items = result.data.records
    if (result.data.cursor)
        do {
            config.params = { ...config.params, cursor: result.data.cursor }
            result = await api.get<PageCursor<T>>(url, config)
            items.push(...result.data.records)
        } while (result.data.cursor !== null)
    return items
}

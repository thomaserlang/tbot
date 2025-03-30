import axios, { AxiosError } from 'axios'

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

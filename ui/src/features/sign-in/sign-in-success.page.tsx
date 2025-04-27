import { PageLoader } from '@/components/page-loader'
import { setAccessToken } from '@/utils/api'
import { Navigate, useLocation } from 'react-router-dom'
import { StringParam, useQueryParam } from 'use-query-params'

export function Component() {
    const { hash } = useLocation()
    const params = new URLSearchParams(hash.substring(1, hash.length))
    const [next] = useQueryParam('next', StringParam)

    if (params.has('access_token')) {
        setAccessToken(params.get('access_token') || '')
    }

    return (
        <>
            <PageLoader />
            <Navigate to={next || '/'} />
        </>
    )
}

import { PageLoader } from '@/components/page-loader'
import { setAccessToken } from '@/utils/api'
import { Navigate, useLocation } from 'react-router-dom'

export function Component() {
    const { hash } = useLocation()
    if (hash.length > 1) {
        setAccessToken(hash.substring(1, hash.length))
    }

    return (
        <>
            <PageLoader />
            <Navigate to={`/`} />
        </>
    )
}

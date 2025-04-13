import { ErrorBox } from '@/components/error-box'
import { PageLoader } from '@/components/page-loader'
import { createContext, useContext } from 'react'
import { useParams } from 'react-router'
import { useGetChannel } from './api/channel.api'
import { Channel } from './types'

const CurrentChannelContext = createContext<Channel | undefined>(undefined)

export function CurrentChannelProvider({
    children,
}: {
    children: React.ReactNode
}) {
    const { channelId } = useParams()
    if (!channelId) {
        throw new Error('channelId is required')
    }
    const { data, error, isLoading } = useGetChannel({ channelId })

    if (isLoading) return <PageLoader />

    if (error) return <ErrorBox errorObj={error} />

    return (
        <CurrentChannelContext.Provider value={data}>
            {data && children}
        </CurrentChannelContext.Provider>
    )
}

export function useCurrentChannel() {
    const currentChannelContext = useContext(CurrentChannelContext)

    if (!currentChannelContext) {
        throw new Error(
            'useCurrentChannel has to be used within <CurrentChannelProvider>'
        )
    }

    return currentChannelContext
}

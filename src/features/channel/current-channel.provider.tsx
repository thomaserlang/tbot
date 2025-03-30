import { createContext, useContext } from 'react'
import { useParams } from 'react-router'
import { useGetChannel } from './api/channel.api'
import { IChannel } from './types'

const CurrentChannelContext = createContext<IChannel | undefined>(undefined)

export function CurrentChannelProvider({
    children,
}: {
    children: React.ReactNode
}) {
    const { channelId } = useParams()
    if (!channelId) {
        throw new Error('channelId is required')
    }
    const { data } = useGetChannel({ channelId })

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

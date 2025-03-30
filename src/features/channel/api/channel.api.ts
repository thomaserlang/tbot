import { api } from '@/utils/api'
import { useQuery } from '@tanstack/react-query'
import { IChannel } from '../types'

interface IParams {
    channelId: string
}

export function getChannelQueryKey(params: IParams) {
    return ['currentChannel', params]
}

export async function getChannel({ channelId }: IParams) {
    const response = await api.get<IChannel>(`/api/2/channels/${channelId}`)
    return response.data
}

export function useGetChannel(params: IParams) {
    return useQuery({
        queryKey: getChannelQueryKey(params),
        queryFn: () => getChannel(params),
    })
}

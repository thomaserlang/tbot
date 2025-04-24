import { getCurrentUserQueryKey } from '@/components/current-user'
import { queryClient } from '@/queryclient'
import { api } from '@/utils/api'
import { useMutation, useQuery } from '@tanstack/react-query'
import { Channel, ChannelId } from '../types'
import { getChannelsQueryKey } from './channels.api'

interface IParams {
    channelId: string
}

export function getChannelQueryKey(params: IParams) {
    return ['currentChannel', params]
}

export async function getChannel({ channelId }: IParams) {
    const response = await api.get<Channel>(`/api/2/channels/${channelId}`)
    return response.data
}

export function useGetChannel(params: IParams) {
    return useQuery({
        queryKey: getChannelQueryKey(params),
        queryFn: () => getChannel(params),
    })
}

export async function deleteChannel(channelId: ChannelId, channelName: string) {
    await api.delete(`/api/2/channels/${channelId}`, {
        params: {
            channel_name: channelName,
        },
    })
}

interface DeleteProps {
    channelId: ChannelId
    channelName: string
}

export function useDeleteChannel({
    onSuccess,
    onError,
}: {
    onSuccess?: (dat: void, variables: DeleteProps) => void
    onError?: (error: unknown, variables: DeleteProps) => void
} = {}) {
    return useMutation({
        mutationFn: ({ channelId, channelName }: DeleteProps) =>
            deleteChannel(channelId, channelName),
        onSuccess: (data, variables) => {
            queryClient.removeQueries({
                queryKey: getChannelQueryKey({
                    channelId: variables.channelId,
                }),
            })
            queryClient.invalidateQueries({
                queryKey: getChannelsQueryKey({}),
            })
            queryClient.invalidateQueries({
                queryKey: getCurrentUserQueryKey(),
            })
            onSuccess?.(data, variables)
        },
        onError,
    })
}

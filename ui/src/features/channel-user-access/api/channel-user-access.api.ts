import { ChannelId } from '@/features/channel/types/channel.types'
import { queryClient } from '@/queryclient'
import { PageCursor } from '@/types/page-cursor.type'
import { api } from '@/utils/api'
import { useInfiniteQuery, useMutation } from '@tanstack/react-query'
import {
    ChannelUserAccess,
    ChannelUserAccessId,
} from '../types/channel-user-access.types'

interface GetParams {}

interface GetProps {
    channelId: ChannelId
    params?: GetParams
}

export function getChannelUsersAccessQueryKey({ channelId, params }: GetProps) {
    return ['users-access', channelId, params]
}

export async function getChannelUsersAccess({
    channelId,
    params,
}: GetProps & { params?: GetParams & { cursor?: string } }) {
    const r = await api.get<PageCursor<ChannelUserAccess>>(
        `/api/2/channels/${channelId}/users-access`,
        {
            params,
        }
    )
    return r.data
}

export function useGetChannelUsersAccess({ channelId, params }: GetProps) {
    return useInfiniteQuery({
        queryKey: getChannelUsersAccessQueryKey({ channelId, params }),
        queryFn: ({ pageParam }) =>
            getChannelUsersAccess({
                channelId,
                params: { ...params, cursor: pageParam },
            }),
        initialPageParam: '',
        getNextPageParam: (lastPage) => lastPage.cursor,
    })
}

interface DeleteProps {
    channelId: ChannelId
    channelUserAccessId: ChannelUserAccessId
}

export async function deleteChannelUserAccess({
    channelUserAccessId,
    channelId,
}: DeleteProps) {
    const r = await api.delete(
        `/api/2/channels/${channelId}/users-access/${channelUserAccessId}`
    )
    return r.data
}

export function useDeleteChannelUserAccess({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: void, variables: DeleteProps) => void
    onError?: (error: unknown, variables: DeleteProps) => void
} = {}) {
    return useMutation({
        mutationFn: deleteChannelUserAccess,
        onSuccess: (data, variables) => {
            queryClient.invalidateQueries({
                queryKey: getChannelUsersAccessQueryKey({
                    channelId: variables.channelId,
                }),
            })
            onSuccess?.(data, variables)
        },
        onError,
    })
}

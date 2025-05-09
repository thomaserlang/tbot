import { Channel, ChannelId } from '@/features/channel/types/channel.types'
import { queryClient } from '@/queryclient'
import { PageCursor } from '@/types/page-cursor.type'
import { api } from '@/utils/api'
import { useInfiniteQuery, useMutation } from '@tanstack/react-query'
import {
    ChannelUserInvite,
    ChannelUserInviteCreate,
    ChannelUserInviteId,
    ChannelUserInviteUpdate,
} from '../types/channel-user-invite.types'

interface GetParams {}

interface GetProps {
    channelId: ChannelId
    params?: GetParams
}

export function getChannelUserInvitesQueryKey(
    channelId: ChannelId,
    params?: GetParams
) {
    return ['channel-user-invite', channelId, params]
}

export async function getChannelUserInvites({
    channelId,
    params,
}: GetProps & { params?: GetParams & { cursor?: string } }) {
    const r = await api.get<PageCursor<ChannelUserInvite>>(
        `/api/2/channels/${channelId}/user-invites`,
        {
            params,
        }
    )
    return r.data
}

export function useGetChannelUserInvites({ channelId, params }: GetProps) {
    return useInfiniteQuery({
        queryKey: getChannelUserInvitesQueryKey(channelId, params),
        queryFn: ({ pageParam }) =>
            getChannelUserInvites({
                channelId,
                params: { ...params, cursor: pageParam },
            }),
        initialPageParam: '',
        getNextPageParam: (lastPage) => lastPage.cursor,
    })
}

interface CreateProps {
    channelId: ChannelId
    data: ChannelUserInviteCreate
}

export async function createChannelUserInvite({
    channelId,
    data,
}: CreateProps) {
    const r = await api.post<ChannelUserInvite>(
        `/api/2/channels/${channelId}/user-invites`,
        data
    )
    return r.data
}

export function useCreateChannelUserInvite({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: ChannelUserInvite, variables: CreateProps) => void
    onError?: (error: unknown, variable: CreateProps) => void
} = {}) {
    return useMutation({
        mutationFn: createChannelUserInvite,
        onSuccess: (data, variables) => {
            queryClient.invalidateQueries({
                queryKey: getChannelUserInvitesQueryKey(variables.channelId),
            })
            onSuccess?.(data, variables)
        },
        onError,
    })
}

interface UpdateProps {
    channelId: ChannelId
    channelUserInviteId: ChannelUserInviteId
    data: ChannelUserInviteUpdate
}
export async function updateChannelUserInvite({
    channelId,
    channelUserInviteId,
    data,
}: UpdateProps) {
    const r = await api.put<ChannelUserInvite>(
        `/api/2/channels/${channelId}/user-invites/${channelUserInviteId}`,
        data
    )
    return r.data
}

export function useUpdateChannelUserInvite({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: ChannelUserInvite, variables: UpdateProps) => void
    onError?: (error: unknown, variable: UpdateProps) => void
}) {
    return useMutation({
        mutationFn: updateChannelUserInvite,
        onSuccess: (data, variables) => {
            queryClient.invalidateQueries({
                queryKey: getChannelUserInvitesQueryKey(variables.channelId),
            })
            onSuccess?.(data, variables)
        },
        onError,
    })
}

interface DeleteProps {
    channelId: ChannelId
    channelUserInviteId: ChannelUserInviteId
}

export async function deleteChannelUserInvite({
    channelId,
    channelUserInviteId,
}: DeleteProps) {
    const r = await api.delete(
        `/api/2/channels/${channelId}/user-invites/${channelUserInviteId}`
    )
    return r.data
}

export function useDeleteChannelUserInvite({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: void, variables: DeleteProps) => void
    onError?: (error: unknown, variable: DeleteProps) => void
} = {}) {
    return useMutation({
        mutationFn: deleteChannelUserInvite,
        onSuccess: (data, variables) => {
            queryClient.invalidateQueries({
                queryKey: getChannelUserInvitesQueryKey(variables.channelId),
            })
            onSuccess?.(data, variables)
        },
        onError,
    })
}

interface AcceptProps {
    channelUserInviteId: ChannelUserInviteId
}

async function acceptChannelUserInvite({ channelUserInviteId }: AcceptProps) {
    const r = await api.post<Channel>(
        `/api/2/channel-user-invites/${channelUserInviteId}/accept`
    )
    return r.data
}

export function useAcceptChannelUserInvite({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: Channel, variables: AcceptProps) => void
    onError?: (error: unknown, variable: AcceptProps) => void
} = {}) {
    return useMutation({
        mutationFn: acceptChannelUserInvite,
        onSuccess,
        onError,
    })
}

import { ChannelId } from '@/features/channel/types'
import { queryClient } from '@/queryclient'
import { PageCursor } from '@/types/page-cursor.type'
import { api } from '@/utils/api'
import { InfiniteData, useMutation, useQuery } from '@tanstack/react-query'
import {
    Command,
    CommandCreate,
    CommandId,
    CommandUpdate,
} from '../types/command.types'
import { getCommandsQueryKey } from './commands.api'

export function getCommandQueryKey(commandId: CommandId) {
    return ['command', commandId]
}

export async function getCommand(channelId: ChannelId, commandId: CommandId) {
    const r = await api.get<Command>(
        `/api/2/channels/${channelId}/commands/${commandId}`
    )
    return r.data
}

interface Props {
    channelId: ChannelId
    commandId: CommandId
}

export function useGetCommand({ channelId, commandId }: Props) {
    return useQuery({
        queryKey: getCommandQueryKey(commandId),
        queryFn: () => getCommand(channelId, commandId),
        enabled: !!channelId && !!commandId,
    })
}

export async function updateCommand(
    channelId: ChannelId,
    commandId: CommandId,
    data: CommandUpdate
) {
    const r = await api.put<Command>(
        `/api/2/channels/${channelId}/commands/${commandId}`,
        data
    )
    return r.data
}

interface UpdateProps {
    channelId: ChannelId
    commandId: CommandId
    data: CommandUpdate
}

export function useUpdateCommand({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: Command, variables: UpdateProps) => void
    onError?: (error: any) => void
} = {}) {
    return useMutation({
        mutationFn: ({ channelId, commandId, data }: UpdateProps) =>
            updateCommand(channelId, commandId, data),
        onSuccess: (data, variables) => {
            queryClient.setQueryData(
                getCommandQueryKey(variables.commandId),
                data
            )
            queryClient.setQueryData(
                getCommandsQueryKey(variables.channelId),
                (oldData: InfiniteData<PageCursor<Command>>) => {
                    const pages = oldData.pages.map((page) => {
                        const newItems = page.records.map((item) =>
                            item.id === variables.commandId ? data : item
                        )
                        return {
                            ...page,
                            records: newItems,
                        }
                    })
                    return {
                        ...oldData,
                        pages,
                    }
                }
            )
            onSuccess?.(data, variables)
        },
        onError,
    })
}

export async function createCommand(channelId: ChannelId, data: CommandCreate) {
    const r = await api.post<Command>(
        `/api/2/channels/${channelId}/commands`,
        data
    )
    return r.data
}

interface CreateProps {
    channelId: ChannelId
    data: CommandCreate
}

export function useCreateCommand({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: Command, variables: CreateProps) => void
    onError?: (error: any) => void
} = {}) {
    return useMutation({
        mutationFn: (data: CreateProps) =>
            createCommand(data.channelId, data.data),
        onSuccess: (data, variables) => {
            queryClient.setQueryData(getCommandQueryKey(data.id), data)
            queryClient.invalidateQueries({
                queryKey: getCommandsQueryKey(variables.channelId),
            })
            onSuccess?.(data, variables)
        },
        onError,
    })
}

export async function deleteCommand(
    channelId: ChannelId,
    commandId: CommandId
): Promise<void> {
    await api.delete(`/api/2/channels/${channelId}/commands/${commandId}`)
}

interface DeleteProps {
    channelId: ChannelId
    commandId: CommandId
}

export function useDeleteCommand({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: void, variables: DeleteProps) => void
    onError?: (error: any) => void
} = {}) {
    return useMutation({
        mutationFn: ({ channelId, commandId }: DeleteProps) =>
            deleteCommand(channelId, commandId),
        onSuccess: (data, variables) => {
            queryClient.removeQueries({
                queryKey: getCommandQueryKey(variables.commandId),
            })
            queryClient.invalidateQueries({
                queryKey: getCommandsQueryKey(variables.channelId),
            })
            onSuccess?.(data, variables)
        },
        onError,
    })
}

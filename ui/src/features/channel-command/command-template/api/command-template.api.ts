import { queryClient } from '@/queryclient'
import { PageCursor } from '@/types/page-cursor.type'
import { api } from '@/utils/api'
import { addRecord, removeRecord, updateRecord } from '@/utils/page-records'
import { InfiniteData, useMutation, useQuery } from '@tanstack/react-query'
import {
    CommandTemplate,
    CommandTemplateCreate,
    CommandTemplateId,
    CommandTemplateUpdate,
} from '../types/command-template.types'
import { getCommandTemplatesQueryKey } from './command-templates.api'

interface GetProps {
    commandTemplateId: CommandTemplateId
}

export function getCommandTemplateQueryKey({ commandTemplateId }: GetProps) {
    return ['command-templates', commandTemplateId]
}

export async function getCommandTemplate({ commandTemplateId }: GetProps) {
    const r = await api.get<CommandTemplate>(
        `/api/2/command-templates/${commandTemplateId}`
    )
    return r.data
}

export function useGetCommandTemplate({ commandTemplateId }: GetProps) {
    return useQuery({
        queryKey: getCommandTemplateQueryKey({ commandTemplateId }),
        queryFn: () => getCommandTemplate({ commandTemplateId }),
        enabled: !!commandTemplateId,
    })
}

interface CreateProps {
    data: CommandTemplateCreate
}

export async function createCommandTemplate({ data }: CreateProps) {
    const r = await api.post<CommandTemplate>('/api/2/command-templates', data)
    queryClient.setQueryData(
        getCommandTemplateQueryKey({ commandTemplateId: r.data.id }),
        data
    )
    queryClient.setQueryData(
        getCommandTemplatesQueryKey(),
        (oldData: InfiniteData<PageCursor<CommandTemplate>>) =>
            addRecord({
                oldData,
                data: r.data,
            })
    )
    queryClient.invalidateQueries({
        queryKey: getCommandTemplatesQueryKey(),
    })
    return r.data
}

export function useCreateCommandTemplate({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: CommandTemplate, variables: CreateProps) => void
    onError?: (error: any, variables: CreateProps) => void
} = {}) {
    return useMutation({
        mutationFn: createCommandTemplate,
        onSuccess,
        onError,
    })
}

interface UpdateProps {
    commandTemplateId: CommandTemplateId
    data: CommandTemplateUpdate
}

export async function updateCommandTemplate({
    commandTemplateId,
    data,
}: UpdateProps) {
    const r = await api.put<CommandTemplate>(
        `/api/2/command-templates/${commandTemplateId}`,
        data
    )
    queryClient.invalidateQueries({
        queryKey: getCommandTemplatesQueryKey(),
    })
    queryClient.setQueryData(
        getCommandTemplatesQueryKey(),
        (oldData: InfiniteData<PageCursor<CommandTemplate>>) =>
            updateRecord({
                oldData,
                data: r.data,
                matchFn: (item) => item.id === commandTemplateId,
            })
    )
    queryClient.setQueryData(
        getCommandTemplateQueryKey({ commandTemplateId }),
        r.data
    )
    return r.data
}

export function useUpdateCommandTemplate({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: CommandTemplate, variables: UpdateProps) => void
    onError?: (error: any, variables: UpdateProps) => void
} = {}) {
    return useMutation({
        mutationFn: updateCommandTemplate,
        onSuccess,
        onError,
    })
}

interface DeleteProps {
    commandTemplateId: CommandTemplateId
}

export async function deleteCommandTemplate({
    commandTemplateId,
}: DeleteProps) {
    await api.delete(`/api/2/command-templates/${commandTemplateId}`)
    queryClient.invalidateQueries({
        queryKey: getCommandTemplatesQueryKey(),
    })
    queryClient.setQueryData(
        getCommandTemplatesQueryKey(),
        (oldData: InfiniteData<PageCursor<CommandTemplate>>) =>
            removeRecord({
                oldData,
                matchFn: (item) => item.id === commandTemplateId,
            })
    )
}

export function useDeleteCommandTemplate({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: void, variables: DeleteProps) => void
    onError?: (error: unknown, variables: DeleteProps) => void
} = {}) {
    return useMutation({
        mutationFn: deleteCommandTemplate,
        onSuccess,
        onError,
    })
}

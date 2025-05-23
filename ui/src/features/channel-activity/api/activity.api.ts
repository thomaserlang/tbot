import { ChannelId } from '@/features/channel/types/channel.types'
import { queryClient } from '@/queryclient'
import { PageCursor } from '@/types/page-cursor.type'
import { api } from '@/utils/api'
import { removeRecord } from '@/utils/page-records'
import { InfiniteData, useMutation } from '@tanstack/react-query'
import { Activity, ActivityId, ActivityUpdate } from '../types/activity.type'
import { getActivitiesQueryKey } from './activities.api'

interface UpdateProps {
    channelId: ChannelId
    activityId: ActivityId
    data: ActivityUpdate
}

export async function updateActivity({
    channelId,
    activityId,
    data,
}: UpdateProps) {
    queryClient.setQueryData(
        getActivitiesQueryKey({ channelId }),
        (oldData: InfiniteData<PageCursor<Activity>> | undefined) => {
            if (!oldData) return oldData
            return {
                ...oldData,
                pages: oldData.pages.map((page) => ({
                    ...page,
                    records: page.records.map((activity) =>
                        activity.id === activityId
                            ? { ...activity, ...data }
                            : activity
                    ),
                })),
            }
        }
    )
    await api.put(`/api/2/channels/${channelId}/activities/${activityId}`, data)
}

export function useUpdateActivity({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: void, variables: UpdateProps) => void
    onError?: (error: unknown, variables: UpdateProps) => void
} = {}) {
    return useMutation({
        mutationFn: updateActivity,
        onSuccess,
        onError,
    })
}

interface DeleteProps {
    channelId: ChannelId
    activityId: ActivityId
}

export async function deleteActivity({ channelId, activityId }: DeleteProps) {
    queryClient.setQueryData(
        getActivitiesQueryKey({ channelId }),
        (oldData: InfiniteData<PageCursor<Activity>>) => {
            removeRecord({
                oldData,
                matchFn: (record) => record.id === activityId,
            })
        }
    )
    try {
        await api.delete(
            `/api/2/channels/${channelId}/activities/${activityId}`
        )
    } catch (error) {
        queryClient.refetchQueries({
            queryKey: getActivitiesQueryKey({ channelId }),
        })
        throw error
    }
}

export function useDeleteActivity({
    onSuccess,
    onError,
}: {
    onSuccess?: (data: void, variables: DeleteProps) => void
    onError?: (error: unknown, variables: DeleteProps) => void
} = {}) {
    return useMutation({
        mutationFn: deleteActivity,
        onSuccess,
        onError,
    })
}

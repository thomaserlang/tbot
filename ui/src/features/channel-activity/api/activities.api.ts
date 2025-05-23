import { ChannelId } from '@/features/channel'
import { queryClient } from '@/queryclient'
import { PageCursor } from '@/types/page-cursor.type'
import { PubSubEvent } from '@/types/pubsub-event.type'
import { api } from '@/utils/api'
import { addRecord, removeRecord, updateRecord } from '@/utils/page-records'
import { InfiniteData, useInfiniteQuery } from '@tanstack/react-query'
import useWebSocket from 'react-use-websocket'
import { Activity } from '../types/activity.type'

export interface GetActivitiesParams {
    type?: string[]
    not_type?: string[]
    min_count?: string[]
}

interface GetProps {
    channelId: ChannelId
    params?: GetActivitiesParams
}

export function getActivitiesQueryKey({ channelId }: GetProps) {
    return ['activities', channelId]
}

export async function getActivities(
    channelId: ChannelId,
    params?: GetActivitiesParams & { cursor?: string }
) {
    const r = await api.get<PageCursor<Activity>>(
        `/api/2/channels/${channelId}/activities`,
        {
            params: {
                per_page: 50,
                ...params,
            },
        }
    )
    return r.data
}

export function useGetActivities({ channelId, params }: GetProps) {
    return useInfiniteQuery({
        queryKey: getActivitiesQueryKey({ channelId, params }),
        queryFn: ({ pageParam }) =>
            getActivities(channelId, { ...params, cursor: pageParam }),
        initialPageParam: '',
        getNextPageParam: (lastPage) => lastPage.cursor ?? undefined,
    })
}

interface WSActivityProps {
    channelId: ChannelId
    params?: GetActivitiesParams
    connect?: boolean
}

export function useWSActivities({
    channelId,
    params,
    connect = true,
}: WSActivityProps) {
    return useWebSocket(
        `/api/2/channels/${channelId}/activity-ws`,

        {
            // @ts-ignore
            queryParams: params,
            shouldReconnect: () => true,
            retryOnError: true,
            reconnectInterval: 1000,
            reconnectAttempts: Infinity,
            onOpen: () => {
                queryClient.refetchQueries({
                    queryKey: getActivitiesQueryKey({
                        channelId,
                        params,
                    }),
                })
            },
            onMessage: (message) => {
                const event = JSON.parse(message.data) as PubSubEvent<Activity>

                queryClient.setQueryData(
                    getActivitiesQueryKey({ channelId, params }),
                    (oldData: InfiniteData<PageCursor<Activity>>) => {
                        if (event.action === 'deleted') {
                            return removeRecord({
                                oldData,
                                matchFn: (item) => item.id === event.data.id,
                            })
                        }

                        if (event.action === 'updated') {
                            return updateRecord({
                                oldData,
                                data: event.data,
                                matchFn: (item) => item.id === event.data.id,
                            })
                        }

                        if (event.action === 'new') {
                            const exists = oldData.pages[0].records.find(
                                (item) => item.id === event.data.id
                            )
                            if (!exists)
                                return addRecord({
                                    oldData,
                                    data: event.data,
                                    maxSize: 100,
                                })
                        }
                    }
                )
            },
        },
        connect
    )
}

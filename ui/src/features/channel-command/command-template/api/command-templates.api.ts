import { PageCursor } from '@/types/page-cursor.type'
import { api } from '@/utils/api'
import { useInfiniteQuery } from '@tanstack/react-query'
import { CommandTemplate } from '../types/command-template.types'

interface GetParams {}

interface GetProps {
    params?: GetParams
}

export function getCommandTemplatesQueryKey({ params = {} }: GetProps = {}) {
    return ['command-templates', params]
}

export async function getCommandTemplates({
    params,
}: GetProps & { params?: GetParams & { cursor?: string } } = {}) {
    const r = await api.get<PageCursor<CommandTemplate>>(
        '/api/2/command-templates',
        {
            params,
        }
    )
    return r.data
}

export function useGetCommandTemplates({ params }: GetProps = {}) {
    return useInfiniteQuery({
        queryKey: getCommandTemplatesQueryKey({ params }),
        queryFn: ({ pageParam }) =>
            getCommandTemplates({
                params: {
                    ...params,
                    cursor: pageParam,
                },
            }),
        initialPageParam: '',
        getNextPageParam: (lastPage) => lastPage.cursor ?? undefined,
    })
}

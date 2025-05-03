import { useGetChannelProviders } from '@/features/channel-providers'
import { ChannelId } from '@/features/channel/types'
import { Provider } from '@/types/provider.type'
import { toastError, toastSuccess } from '@/utils/toast'
import { Button, Flex } from '@mantine/core'
import { useHotkeys } from '@mantine/hooks'
import { useBanUser, useUnbanUser } from '../api/chat-ban.api'
import { ProviderViewerId } from '../types/viewer.type'

interface IProps {
    channelId: ChannelId
    provider: Provider
    providerViewerId: ProviderViewerId
}

export function ModerationButtons(props: IProps) {
    const channelProviders = useGetChannelProviders({
        channelId: props.channelId,
    })
    const channelProvider = channelProviders.data?.find(
        (provider) => provider.provider === props.provider
    )
    if (!channelProvider) return null

    return (
        <Flex gap="0.5rem">
            <BanButton {...props} />
            <TimeoutButton {...props} />
            <UnbanButton {...props} />
        </Flex>
    )
}

function BanButton(props: IProps) {
    const channelProviders = useGetChannelProviders({
        channelId: props.channelId,
    })
    const banUser = useBanUser({
        onSuccess: () => {
            toastSuccess('User banned successfully')
        },
        onError: (error) => {
            toastError(error)
        },
    })
    useHotkeys([['B', () => doBanUser()]])
    const doBanUser = () => {
        channelProviders.data
            ?.filter((provider) => provider.provider === props.provider)
            .map((channelProvider) => {
                banUser.mutate({
                    ...props,
                    channelProviderId: channelProvider.id,
                })
            })
    }

    return (
        <Button
            variant="default"
            onClick={doBanUser}
            loading={banUser.isPending}
        >
            Ban
        </Button>
    )
}

function TimeoutButton(props: IProps) {
    const channelProviders = useGetChannelProviders({
        channelId: props.channelId,
    })
    const banUser = useBanUser({
        onSuccess: () => {
            toastSuccess('User timed out successfully')
        },
        onError: (error) => {
            toastError(error)
        },
    })
    useHotkeys([['T', () => doTimeoutUser()]])

    const doTimeoutUser = () => {
        channelProviders.data
            ?.filter((provider) => provider.provider === props.provider)
            .map((channelProvider) => {
                banUser.mutate({
                    ...props,
                    channelProviderId: channelProvider.id,
                    banDuration: 600,
                })
            })
    }

    return (
        <Button
            variant="default"
            onClick={doTimeoutUser}
            loading={banUser.isPending}
        >
            Timeout
        </Button>
    )
}

function UnbanButton(props: IProps) {
    const channelProviders = useGetChannelProviders({
        channelId: props.channelId,
    })
    const unbanUser = useUnbanUser({
        onSuccess: () => {
            toastSuccess('User unbanned successfully')
        },
        onError: (error) => {
            toastError(error)
        },
    })
    const doUnbanUser = () => {
        console.log(channelProviders.data)
        channelProviders.data
            ?.filter((provider) => provider.provider === props.provider)
            .map((channelProvider) => {
                unbanUser.mutate({
                    ...props,
                    channelProviderId: channelProvider.id,
                })
            })
    }
    useHotkeys([['U', () => doUnbanUser()]])

    return (
        <Button
            variant="default"
            onClick={doUnbanUser}
            loading={unbanUser.isPending}
        >
            Unban
        </Button>
    )
}

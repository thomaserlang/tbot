import { ErrorBox } from '@/components/error-box'
import { PageLoader } from '@/components/page-loader'
import { providerInfo } from '@/constants'
import { ChannelId } from '@/features/channel'
import { useGetChannelProviders } from '@/features/channel-provider'
import { Divider, Flex, Paper, ScrollArea } from '@mantine/core'
import { useLocalStorage } from '@mantine/hooks'
import { IconChevronDown, IconChevronRight } from '@tabler/icons-react'
import { Fragment } from 'react/jsx-runtime'
import { DashboardChannelProvider } from './dashboard-channel-provider'

interface Props {
    channelId: ChannelId
}

export function DashboardProviders({ channelId }: Props) {
    const channelProviders = useGetChannelProviders({
        channelId,
        options: {
            refetchInterval: 5000,
        },
    })
    const [collapsed, setCollapsed] = useLocalStorage({
        key: 'dashboard-channel-providers-collapsed',
        defaultValue: false,
    })

    if (channelProviders.isLoading) return <PageLoader />
    if (channelProviders.error)
        return <ErrorBox errorObj={channelProviders.error} />

    return (
        <Paper withBorder p="0.5rem">
            <Flex direction="row" gap="1rem">
                {!collapsed ? (
                    <IconChevronDown
                        title="Collapse"
                        onClick={() => {
                            setCollapsed(!collapsed)
                        }}
                        style={{
                            cursor: 'pointer',
                        }}
                        size={24}
                    />
                ) : (
                    <IconChevronRight
                        title="Expand"
                        onClick={() => {
                            setCollapsed(!collapsed)
                        }}
                        style={{
                            cursor: 'pointer',
                        }}
                        size={24}
                    />
                )}

                <ScrollArea>
                    <Flex direction="row" gap="1rem">
                        <Divider orientation="vertical" />
                        {channelProviders.data
                            ?.filter((f) => providerInfo[f.provider].stream)
                            .map((channelProvider) => (
                                <Fragment key={channelProvider.id}>
                                    <DashboardChannelProvider
                                        key={channelProvider.id}
                                        channelProvider={channelProvider}
                                        collapsed={collapsed}
                                    />
                                    <Divider orientation="vertical" />
                                </Fragment>
                            ))}
                    </Flex>
                </ScrollArea>
            </Flex>
        </Paper>
    )
}

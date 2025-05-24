import { ErrorBox } from '@/components/error-box'
import { PageLoader } from '@/components/page-loader'
import { providerInfo } from '@/constants'
import { ChannelId } from '@/features/channel'
import { useGetChannelProviders } from '@/features/channel-provider'
import { ActionIcon, Box, Divider, Flex, ScrollArea } from '@mantine/core'
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
        defaultValue: true,
    })

    if (channelProviders.isLoading) return <PageLoader />
    if (channelProviders.error)
        return <ErrorBox errorObj={channelProviders.error} />

    return (
        <Flex direction="row" gap="0.5rem">
            <Box>
                {!collapsed ? (
                    <ActionIcon
                        title="Collapse"
                        variant="subtle"
                        size="md"
                        color="gray"
                        onClick={() => {
                            setCollapsed(!collapsed)
                        }}
                    >
                        <IconChevronDown size={22} />
                    </ActionIcon>
                ) : (
                    <ActionIcon
                        variant="subtle"
                        size="md"
                        onClick={() => {
                            setCollapsed(!collapsed)
                        }}
                        title="Expand"
                        color="gray"
                    >
                        <IconChevronRight size={22} />
                    </ActionIcon>
                )}
            </Box>

            <ScrollArea>
                <Flex direction="row" gap="1rem">
                    <Divider orientation="vertical" />
                    {channelProviders.data
                        ?.filter((f) => providerInfo[f.provider].stream)
                        .map((channelProvider) => (
                            <Fragment key={channelProvider.id}>
                                <Flex>
                                    <Box w="250px">
                                        <DashboardChannelProvider
                                            channelProvider={channelProvider}
                                            collapsed={collapsed}
                                        />
                                    </Box>
                                </Flex>
                                <Divider orientation="vertical" />
                            </Fragment>
                        ))}
                </Flex>
            </ScrollArea>
        </Flex>
    )
}

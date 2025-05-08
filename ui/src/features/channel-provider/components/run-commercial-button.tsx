import { providerInfo } from '@/constants/providers-info.constants'
import { ChannelId } from '@/features/channel/types'
import { toastPromise } from '@/utils/toast'
import { Button, Menu } from '@mantine/core'
import { IconChevronDown } from '@tabler/icons-react'
import { useRunCommercial } from '../api/channel-provider-commercial'
import { useGetChannelProviders } from '../api/channel-providers.api'

interface Props {
    channelId: ChannelId
}

export function RunCommercialButton({ channelId }: Props) {
    const channelProviders = useGetChannelProviders({ channelId })
    const runCommercial = useRunCommercial()

    const run = (length: number) => {
        channelProviders.data
            ?.filter((p) => p.stream_live)
            .forEach((p) => {
                toastPromise({
                    promise: runCommercial.mutateAsync({
                        channelId: p.channel_id,
                        channelProviderId: p.id,
                        data: {
                            length: length,
                        },
                    }),
                    loading: {
                        title: providerInfo[p.provider].name,
                        message: `Starting ads`,
                    },
                    success: {
                        title: providerInfo[p.provider].name,
                        message: `Ads started`,
                    },
                    error: {
                        title: providerInfo[p.provider].name,
                    },
                })
            })
    }

    return (
        <Menu shadow="md" width={200}>
            <Menu.Target>
                <Button
                    loading={runCommercial.isPending}
                    rightSection={<IconChevronDown size={14} />}
                    variant="default"
                >
                    Run Ads
                </Button>
            </Menu.Target>
            <Menu.Dropdown>
                <Menu.Item
                    onClick={() => {
                        run(30)
                    }}
                >
                    30 Seconds
                </Menu.Item>
                <Menu.Item
                    onClick={() => {
                        run(60)
                    }}
                >
                    1 Minute
                </Menu.Item>
                <Menu.Item
                    onClick={() => {
                        run(120)
                    }}
                >
                    2 Minutes
                </Menu.Item>
                <Menu.Item
                    onClick={() => {
                        run(180)
                    }}
                >
                    3 Minutes
                </Menu.Item>
            </Menu.Dropdown>
        </Menu>
    )
}

import { RelativeTimeUpdater } from '@/components/relative-time-updater'
import { providerInfo } from '@/constants'
import { ChatMessage } from '@/features/channel-combined-chat'
import { Box, Divider, Flex, Text } from '@mantine/core'
import { Fragment } from 'react/jsx-runtime'

interface Props {
    notices: ChatMessage[]
}

export function NoticeFeedList({ notices }: Props) {
    return (
        <Flex direction="column" gap="0.75rem">
            {notices.map((notice) => (
                <Fragment key={notice.id}>
                    <Flex direction="column">
                        <Flex align="center" gap="0.25rem">
                            <Box
                                c={providerInfo[notice.provider].color}
                                mb="-0.5rem"
                            >
                                {providerInfo[notice.provider].icon}
                            </Box>
                            <Text
                                size="xs"
                                c="dimmed"
                                title={notice.created_at}
                            >
                                <RelativeTimeUpdater dt={notice.created_at} />
                            </Text>
                        </Flex>

                        <Text>{notice.message}</Text>
                    </Flex>

                    <Divider />
                </Fragment>
            ))}
        </Flex>
    )
}

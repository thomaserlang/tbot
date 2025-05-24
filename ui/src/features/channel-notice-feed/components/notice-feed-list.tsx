import { RelativeTimeUpdater } from '@/components/relative-time-updater'
import { providerInfo } from '@/constants'
import { ChatMessage } from '@/features/channel-chat'
import { ChatMessageLine } from '@/features/channel-chat/components/chat-message-line'
import { Box, Divider, Flex, Text } from '@mantine/core'
import { Fragment } from 'react/jsx-runtime'

interface Props {
    notices: ChatMessage[]
}

export function NoticeFeedList({ notices }: Props) {
    return (
        <Flex direction="column" gap="0.5rem">
            {notices.map((notice) => (
                <Fragment key={notice.id}>
                    <Flex direction="column" p="0 1rem">
                        <Flex align="center" gap="0.25rem">
                            <Box
                                c={providerInfo[notice.provider].color}
                                mb="-0.5rem"
                            >
                                {providerInfo[notice.provider].icon?.({
                                    size: 18,
                                })}
                            </Box>
                            <Text
                                size="xs"
                                c="dimmed"
                                title={notice.created_at}
                            >
                                <RelativeTimeUpdater date={notice.created_at} />
                            </Text>
                        </Flex>

                        <Text>{notice.notice_message}</Text>
                        {notice.message_parts.length > 0 && (
                            <ChatMessageLine
                                chatMessage={notice}
                                hideProviderLogo
                                hideTime
                                hideBadges
                            />
                        )}
                    </Flex>

                    <Divider />
                </Fragment>
            ))}
        </Flex>
    )
}

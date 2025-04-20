import { ChatMessage } from '@/features/channel-combined-chat/types/chat-message.type'
import { providers } from '@/types/provider.type'
import { Box, Flex, Text } from '@mantine/core'

interface Props {
    notices: ChatMessage[]
}

export function NoticeFeedList({ notices }: Props) {
    return (
        <Flex direction="column" gap="1rem">
            {notices.map((notice) => (
                <Flex gap="0.25rem" align="center" key={notice.id}>
                    <Text c="dimmed" title={notice.created_at}>
                        {new Date(notice.created_at).toLocaleTimeString([], {
                            hour: '2-digit',
                            minute: '2-digit',
                            hour12: false,
                        })}
                    </Text>
                    <Box c={providers[notice.provider].color}>
                        {providers[notice.provider].chat_icon}
                    </Box>
                    <Text>{notice.message}</Text>
                </Flex>
            ))}
        </Flex>
    )
}

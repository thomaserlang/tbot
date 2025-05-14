import { Divider, Flex, Text } from '@mantine/core'
import { ChatMessage, ChatMessageSubType } from '../types/chat-message.type'
import { AssembleParts } from './assemble-parts'
import { ChatMessageLine } from './chat-message-line'
import { ProviderLogo } from './provider-logo'

interface Props {
    chatMessage: ChatMessage
    color?: string
}

export function ChatNoticeLine({ chatMessage, color }: Props) {
    return (
        <Flex gap="0.25rem">
            <Divider
                size="0.5rem"
                orientation="vertical"
                color={color || subTypeToColor(chatMessage.sub_type)}
            />

            <Flex direction="column" pb="0.1rem" pt="0.1rem">
                <Flex gap="0.1rem">
                    <ProviderLogo provider={chatMessage.provider} />

                    <Text component="span" c="dimmed">
                        <AssembleParts parts={chatMessage.notice_parts} />
                    </Text>
                </Flex>

                {chatMessage.parts.length > 0 && (
                    <ChatMessageLine
                        chatMessage={chatMessage}
                        hideProviderLogo
                    />
                )}
            </Flex>
        </Flex>
    )
}

function subTypeToColor(subType: ChatMessageSubType) {
    switch (subType) {
        case 'sub':
        case 'resub':
        case 'sub_gift':
        case 'community_sub_gift':
        case 'gift_paid_upgrade':
        case 'prime_paid_upgrade':
        case 'pay_it_forward':
            return '#228be6'
        case 'announcement':
            return '#4c6ef5'
    }
}

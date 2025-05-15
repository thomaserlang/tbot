import { Box, Flex, Text } from '@mantine/core'
import { ChatMessage, ChatMessageSubType } from '../types/chat-message.type'
import { AssembleParts } from './assemble-parts'
import { ChatMessageLine } from './chat-message-line'
import classes from './chat-notice.module.css'
import { ProviderLogo } from './provider-logo'

interface Props {
    chatMessage: ChatMessage
}

export function ChatNoticeLine({ chatMessage }: Props) {
    return (
        <Flex
            gap="0.5rem"
            className={`${classes.notice} ${subTypeToClassName(
                chatMessage.sub_type
            )}`}
        >
            <Box className={classes.verticalLine} />

            <Flex direction="column" className={classes.text}>
                <Flex gap="0.1rem">
                    <ProviderLogo provider={chatMessage.provider} />

                    <Text component="span">
                        <AssembleParts
                            parts={chatMessage.notice_parts}
                            subType={chatMessage.sub_type}
                            channelId={chatMessage.channel_id}
                            provider={chatMessage.provider}
                            providerUserId={chatMessage.provider_id}
                        />
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

function subTypeToClassName(subType: ChatMessageSubType) {
    switch (subType) {
        case 'cheer':
        case 'sub':
        case 'resub':
        case 'sub_gift':
        case 'community_sub_gift':
        case 'gift_paid_upgrade':
        case 'prime_paid_upgrade':
        case 'pay_it_forward':
        case 'newSponsorEvent':
        case 'superChatEvent':
        case 'superStickerEvent':
        case 'membershipGiftingEvent':
        case 'giftMembershipReceivedEvent':
        case 'gift':
            return `${classes['gold-border']} ${classes['gold-notice']}`
        case 'announcement':
            return classes['announcement-notice']
    }
}

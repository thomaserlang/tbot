import { Avatar, Flex, Modal, StyleProp, Text } from '@mantine/core'
import { IconSelector } from '@tabler/icons-react'
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useCurrentChannel } from '../current-channel.provider'
import { SelectChannel } from './select-channel'

interface Props {
    nameFw?: StyleProp<React.CSSProperties['fontWeight']>
    maw?: StyleProp<React.CSSProperties['maxWidth']>
    w?: StyleProp<React.CSSProperties['width']>
}

export function CurrentChannelCard({ nameFw, maw = 160, w }: Props) {
    const [showModal, setShowModal] = useState(false)
    const navigate = useNavigate()
    const channel = useCurrentChannel()
    return (
        <>
            <Flex
                align="center"
                gap="0.5rem"
                style={{
                    cursor: 'pointer',
                    userSelect: 'none',
                }}
                onClick={() => {
                    setShowModal(true)
                }}
            >
                <Avatar color="blue" size="sm" name={channel.display_name} />
                <Text truncate="end" maw={w || maw} w={w} size="md" fw={nameFw}>
                    {channel.display_name}
                </Text>
                <IconSelector size={20} />
            </Flex>
            <Modal
                size="lg"
                onClose={() => setShowModal(false)}
                opened={showModal}
                title="Pick a channel"
            >
                {showModal && (
                    <SelectChannel
                        onSelect={(channel) => {
                            setShowModal(false)
                            navigate(`/channels/${channel.id}`)
                        }}
                    />
                )}
            </Modal>
        </>
    )
}

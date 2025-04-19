import { Badge, Box, NavLink, Paper } from '@mantine/core'
import {
    IconBlocks,
    IconClock,
    IconCoin,
    IconHome,
    IconLink,
    IconLock,
    IconMessage,
    IconPokerChip,
    IconQuote,
    IconShieldCog,
} from '@tabler/icons-react'
import { NavLink as RouterNavLink } from 'react-router-dom'
import { useGetProviders } from '../channel-providers/channel-providers.api'
import { CurrentChannelCard } from './components/current-channel-card'
import { useCurrentChannel } from './current-channel.provider'
import { Channel } from './types'

export function ChannelNavbar() {
    const channel = useCurrentChannel()
    return (
        <>
            <Paper withBorder p="0.5rem" radius="md" m="0.5rem" mb="1rem">
                <CurrentChannelCard nameFw={500} w="100%" />
            </Paper>
            <Box pl="0.5rem" pr="0.5rem">
                <NavLink
                    component={RouterNavLink}
                    to={`/channels/${channel.id}`}
                    label="Dashboard"
                    leftSection={<IconHome size={20} />}
                    end
                />
                <ProvidersNavbar channel={channel} />
                <NavLink
                    component={RouterNavLink}
                    to={`/channels/${channel.id}/combined-chat`}
                    label="Combined Chat"
                    leftSection={<IconMessage size={20} />}
                />
                <NavLink
                    component={RouterNavLink}
                    to={`/channels/${channel.id}/commands`}
                    label="Commands"
                    leftSection={<IconBlocks size={20} />}
                />
                <NavLink
                    component={RouterNavLink}
                    to={`/channels/${channel.id}/timers`}
                    label="Timers"
                    leftSection={<IconClock size={20} />}
                />
                <NavLink
                    component={RouterNavLink}
                    to={`/channels/${channel.id}/chat-filters`}
                    label="Chat Filters"
                    leftSection={<IconShieldCog size={20} />}
                />
                <NavLink
                    component={RouterNavLink}
                    to={`/channels/${channel.id}/quotes`}
                    label="Quotes"
                    leftSection={<IconQuote size={20} />}
                    disabled
                />
                <NavLink
                    component={RouterNavLink}
                    to={`/channels/${channel.id}/gambling`}
                    label="Gambling"
                    leftSection={<IconCoin size={20} />}
                    disabled
                >
                    <NavLink
                        component={RouterNavLink}
                        to={`/channels/${channel.id}/gambling/points`}
                        label="Points Settings"
                        leftSection={<IconPokerChip size={20} />}
                    />
                    <NavLink
                        component={RouterNavLink}
                        to={`/channels/${channel.id}/gambling/slots`}
                        label="Slots Settings"
                        leftSection={<IconPokerChip size={20} />}
                    />
                    <NavLink
                        component={RouterNavLink}
                        to={`/channels/${channel.id}/gambling/roulette`}
                        label="Roulette Settings"
                        leftSection={<IconPokerChip size={20} />}
                    />
                </NavLink>
                <NavLink
                    component={RouterNavLink}
                    to={`/channels/${channel.id}/user-access`}
                    label="User Access"
                    leftSection={<IconLock size={20} />}
                    disabled
                />
            </Box>
        </>
    )
}

function ProvidersNavbar({ channel }: { channel: Channel }) {
    const { data } = useGetProviders({
        channelId: channel.id,
    })

    let warnings = 0
    for (const provider of data ?? []) {
        if (provider.scope_needed) warnings++
        if (provider.bot_provider?.scope_needed) warnings++
    }

    return (
        <NavLink
            component={RouterNavLink}
            to={`/channels/${channel.id}/providers`}
            label="Providers"
            leftSection={<IconLink size={20} />}
            rightSection={
                warnings > 0 && (
                    <Badge title="Extra permissions required" color="red">
                        {warnings}
                    </Badge>
                )
            }
        />
    )
}

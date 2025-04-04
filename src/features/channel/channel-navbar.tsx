import { Box, NavLink, Paper } from '@mantine/core'
import {
    IconBlocks,
    IconClock,
    IconCoin,
    IconFilter,
    IconHome,
    IconLink,
    IconLock,
    IconPokerChip,
    IconQuote,
    IconWood,
} from '@tabler/icons-react'
import { NavLink as RouterNavLink } from 'react-router-dom'
import { CurrentChannelCard } from './components/current-channel-card'
import { useCurrentChannel } from './current-channel.provider'

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
                <NavLink
                    component={RouterNavLink}
                    to={`/channels/${channel.id}/logviewer`}
                    label="Logviewer"
                    leftSection={<IconWood size={20} />}
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
                    to={`/channels/${channel.id}/filters`}
                    label="Filters"
                    leftSection={<IconFilter size={20} />}
                />
                <NavLink
                    component={RouterNavLink}
                    to={`/channels/${channel.id}/quotes`}
                    label="Quotes"
                    leftSection={<IconQuote size={20} />}
                />
                <NavLink
                    component={RouterNavLink}
                    to={`/channels/${channel.id}/gambling`}
                    label="Gambling"
                    leftSection={<IconCoin size={20} />}
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
                />
                <NavLink
                    component={RouterNavLink}
                    to={`/channels/${channel.id}/providers`}
                    label="Providers"
                    leftSection={<IconLink size={20} />}
                />
            </Box>
        </>
    )
}

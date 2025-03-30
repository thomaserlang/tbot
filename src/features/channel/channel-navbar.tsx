import { Box, NavLink, Paper } from '@mantine/core'
import { IconHome, IconLink } from '@tabler/icons-react'
import { NavLink as RouterNavLink } from 'react-router-dom'
import { CurrentChannelCard } from './components/current-channel-card'
import { useCurrentChannel } from './current-channel.provider'

export function ChannelNavbar() {
    const channel = useCurrentChannel()
    return (
        <>
            <Paper withBorder p="0.5rem" radius="md" m="0.5rem" mb="1rem">
                <CurrentChannelCard nameFw={500} w={200} />
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
                    to={`/channels/${channel.id}/providers`}
                    label="Providers"
                    leftSection={<IconLink size={20} />}
                />
            </Box>
        </>
    )
}

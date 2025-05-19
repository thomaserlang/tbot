import { Box, NavLink } from '@mantine/core'
import { IconBlocks, IconHome, IconRobot } from '@tabler/icons-react'
import { NavLink as RouterNavLink } from 'react-router-dom'

export function AdminNavbar() {
    return (
        <Box pl="0.5rem" pr="0.5rem" mt="0.5rem">
            <NavLink
                component={RouterNavLink}
                to={`/admin`}
                label="Dashboard"
                leftSection={<IconHome size={20} />}
                end
            />
            <NavLink
                component={RouterNavLink}
                to={`/admin/system-provider-bots`}
                label="System Provider Bots"
                leftSection={<IconRobot size={20} />}
            />
            <NavLink
                component={RouterNavLink}
                to={`/admin/command-templates`}
                label="Command Templates"
                leftSection={<IconBlocks size={20} />}
            />
        </Box>
    )
}

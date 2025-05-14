import { providerInfo } from '@/constants/providers-info.constants'
import { Provider } from '@/types/provider.type'
import { Box } from '@mantine/core'
import classes from './chat-message-line.module.css'

interface Props {
    provider: Provider
}

export function ProviderLogo({ provider }: Props) {
    return (
        <Box
            component="span"
            className={classes.provider}
            title={providerInfo[provider].name || ''}
            c={providerInfo[provider].color}
        >
            {providerInfo[provider].icon}
        </Box>
    )
}

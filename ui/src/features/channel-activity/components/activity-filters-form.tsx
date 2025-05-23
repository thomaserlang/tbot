import { useCurrentUserSettings } from '@/components/current-user/current-user-settings.provider'
import { ErrorBox } from '@/components/error-box'
import { PageLoader } from '@/components/page-loader'
import { providerInfo } from '@/constants/providers-info.constants'
import { Provider } from '@/types/provider.type'
import {
    Badge,
    Box,
    Button,
    Flex,
    NumberInput,
    Paper,
    SimpleGrid,
    Switch,
    Text,
} from '@mantine/core'
import { useGetActivityTypes } from '../api/activity-types.api'
import { ActivityTypeName } from '../types/activity-type.type'

export function ActivityFiltersForm() {
    const types = useGetActivityTypes()

    if (types.isLoading) return <PageLoader />
    if (types.error) return <ErrorBox errorObj={types.error} />
    if (!types.data) return

    const providers = [...new Set(types.data.map((t) => t.provider))]

    return (
        <Flex gap="1rem" direction="column">
            {providers.map((p) => (
                <Box key={p}>
                    <Paper withBorder p="1rem">
                        <ChannelProviderTypes
                            provider={p}
                            activityTypes={types.data}
                        />
                    </Paper>
                </Box>
            ))}
        </Flex>
    )
}

function ChannelProviderTypes({
    provider,
    activityTypes,
}: {
    provider: Provider
    activityTypes: ActivityTypeName[]
}) {
    const { settings, updateSettings } = useCurrentUserSettings()
    return (
        <Flex gap="1rem" direction="column">
            <Flex gap="0.25rem " align="center">
                {providerInfo[provider].icon?.({ size: 18 })}
                <Text fw={500}>{providerInfo[provider].name}</Text>
                <Button
                    ml="auto"
                    variant="default"
                    size="compact-sm"
                    onClick={() => {
                        const notTypes = settings.activity_feed_not_types || []
                        const allTypes = activityTypes
                            .filter((f) => f.provider === provider)
                            .map((f) => f.name)

                        const allEnabled = allTypes.every(
                            (name) => !notTypes.includes(name)
                        )

                        if (allEnabled) {
                            updateSettings({
                                activity_feed_not_types: [
                                    ...notTypes.filter(
                                        (name) => !allTypes.includes(name)
                                    ),
                                    ...allTypes,
                                ],
                            })
                        } else {
                            updateSettings({
                                activity_feed_not_types: notTypes.filter(
                                    (name) => !allTypes.includes(name)
                                ),
                            })
                        }
                    }}
                >
                    Toggle All
                </Button>
            </Flex>
            <SimpleGrid cols={{ base: 1, sm: 2 }}>
                {activityTypes
                    .filter((f) => f.provider == provider)
                    .map((activityType) => (
                        <Flex
                            gap="0.5rem"
                            key={activityType.name}
                            align="center"
                        >
                            <Switch
                                checked={
                                    !(
                                        settings.activity_feed_not_types || []
                                    ).includes(activityType.name)
                                }
                                onChange={(event) => {
                                    if (event.currentTarget.checked) {
                                        updateSettings({
                                            activity_feed_not_types:
                                                settings.activity_feed_not_types.filter(
                                                    (name) =>
                                                        name !==
                                                        activityType.name
                                                ),
                                        })
                                    } else {
                                        updateSettings({
                                            activity_feed_not_types: [
                                                ...settings.activity_feed_not_types,
                                                activityType.name,
                                            ],
                                        })
                                    }
                                }}
                                label={
                                    <Flex gap="0.5rem" align="center">
                                        <Badge
                                            color={activityType.color}
                                        ></Badge>{' '}
                                        {activityType.display_name}
                                    </Flex>
                                }
                            />
                            {activityType.filter_min_count && (
                                <NumberInput
                                    ml="auto"
                                    w="4rem"
                                    size="xs"
                                    onBlur={(event) => {
                                        const value =
                                            parseInt(
                                                String(
                                                    event.currentTarget.value
                                                )
                                            ) || 0
                                        updateSettings({
                                            activity_feed_type_min_count: {
                                                ...settings.activity_feed_type_min_count,
                                                [activityType.name]: value,
                                            },
                                        })
                                    }}
                                    value={
                                        settings.activity_feed_type_min_count?.[
                                            activityType.name
                                        ] || 0
                                    }
                                />
                            )}
                        </Flex>
                    ))}
            </SimpleGrid>
        </Flex>
    )
}

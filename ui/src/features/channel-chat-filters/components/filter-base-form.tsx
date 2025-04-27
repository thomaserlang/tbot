import { accessLevelInfo, providerInfo } from '@/constants'
import {
    Flex,
    NumberInput,
    Select,
    SimpleGrid,
    Switch,
    TextInput,
    Title,
} from '@mantine/core'
import { UseFormReturnType } from '@mantine/form'
import { IconHourglassEmpty, IconLock } from '@tabler/icons-react'
import { ChatFilterRequestBase } from '../filter.types'

interface Props {
    form: UseFormReturnType<ChatFilterRequestBase>
}

export function FilterForm({ form }: Props) {
    return (
        <Flex direction="column" gap="1rem">
            <Flex>
                <Switch
                    label="Enabled"
                    key={form.key('enabled')}
                    {...form.getInputProps('enabled', { type: 'checkbox' })}
                />
            </Flex>

            <SimpleGrid cols={{ base: 2, md: 3 }}>
                <Select
                    leftSection={<IconLock size={16} />}
                    label="Exclude"
                    data={Object.values(accessLevelInfo).map((accessLevel) => ({
                        value: accessLevel.value.toString(),
                        label: accessLevel.label,
                    }))}
                    key={form.key('exclude_access_level')}
                    {...form.getInputProps('exclude_access_level')}
                />
                <Select
                    label="Provider"
                    data={Object.values({
                        all: { key: 'all', name: 'All', chat: true },
                        ...providerInfo,
                    })
                        .filter((t) => t.chat)
                        .map((value) => ({
                            value: value.key,
                            label: value.name,
                        }))}
                    key={form.key('provider')}
                    {...form.getInputProps('provider')}
                />
            </SimpleGrid>

            <Flex gap="0.5rem" direction="column">
                <Title order={5}>Warning</Title>

                <Switch
                    label="Warning enabled"
                    key={form.key('warning_enabled')}
                    {...form.getInputProps('warning_enabled', {
                        type: 'checkbox',
                    })}
                />

                <TextInput
                    label="Warning message"
                    key={form.key('warning_message')}
                    {...form.getInputProps('warning_message')}
                />

                <SimpleGrid cols={{ base: 2, md: 3 }}>
                    <NumberInput
                        leftSection={<IconHourglassEmpty size={16} />}
                        label="Warning expires after"
                        key={form.key('warning_expire_duration')}
                        allowNegative={false}
                        suffix=" seconds"
                        {...form.getInputProps('warning_expire_duration')}
                    />
                </SimpleGrid>
            </Flex>

            <Flex gap="0.5rem" direction="column">
                <Title order={5}>Timeout</Title>

                <TextInput
                    label="Timeout message"
                    key={form.key('timeout_message')}
                    {...form.getInputProps('timeout_message')}
                />

                <SimpleGrid cols={{ base: 2, md: 3 }}>
                    <NumberInput
                        leftSection={<IconHourglassEmpty size={16} />}
                        label="Timeout duration"
                        key={form.key('timeout_duration')}
                        allowNegative={false}
                        suffix=" seconds"
                        {...form.getInputProps('timeout_duration')}
                    />
                </SimpleGrid>
            </Flex>
        </Flex>
    )
}

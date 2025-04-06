import { accessLevelLabels } from '@/types/access-level.type'
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
                    key={form.key('exclude_access_level')}
                    data={Object.keys(accessLevelLabels).map((key) => ({
                        value: key,
                        label: accessLevelLabels[key],
                    }))}
                    {...form.getInputProps('exclude_access_level')}
                    defaultValue={form.values.exclude_access_level?.toString()}
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

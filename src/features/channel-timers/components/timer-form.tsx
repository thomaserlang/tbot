import { providerLabels } from '@/types/provider.type'
import {
    ActionIcon,
    Flex,
    InputLabel,
    NumberInput,
    Select,
    SimpleGrid,
    Switch,
    TextInput,
} from '@mantine/core'
import { UseFormReturnType } from '@mantine/form'
import { IconClock, IconPlus, IconX } from '@tabler/icons-react'
import {
    timerActiveModeLabels,
    TimerCreate,
    timerPickModeLabels,
    TimerUpdate,
} from '../timer.types'

interface Props {
    form: UseFormReturnType<TimerCreate> | UseFormReturnType<TimerUpdate>
}

export function TimerForm({ form }: Props) {
    return (
        <Flex direction="column" gap="1rem">
            <TextInput
                label="Name"
                key={form.key('name')}
                {...form.getInputProps('name')}
            />

            <SimpleGrid cols={{ base: 2, md: 3 }}>
                <NumberInput
                    leftSection={<IconClock size={16} />}
                    label="Interval"
                    key={form.key('interval')}
                    allowNegative={false}
                    suffix=" minutes"
                    {...form.getInputProps('interval')}
                />

                <Select
                    label="Active when"
                    key={form.key('active_mode')}
                    data={Object.keys(timerActiveModeLabels).map((key) => ({
                        value: key,
                        label: timerActiveModeLabels[key],
                    }))}
                    {...form.getInputProps('active_mode')}
                />

                <Select
                    label="Pick mode"
                    key={form.key('pick_mode')}
                    data={Object.keys(timerPickModeLabels).map((key) => ({
                        value: key,
                        label: timerPickModeLabels[key],
                    }))}
                    {...form.getInputProps('pick_mode')}
                />
                <Select
                    label="Provider"
                    key={form.key('provider')}
                    data={Object.keys(providerLabels).map((key) => ({
                        value: key,
                        label: providerLabels[key],
                    }))}
                    {...form.getInputProps('provider')}
                />
            </SimpleGrid>

            <Flex>
                <Switch
                    label="Enabled"
                    key={form.key('enabled')}
                    style={{ cursor: 'pointer' }}
                    {...form.getInputProps('enabled', { type: 'checkbox' })}
                />
            </Flex>

            <Flex direction="column" gap="0.5rem">
                <InputLabel>Messages</InputLabel>
                {form.getValues().messages?.map((_, index) => (
                    <Flex gap="0.5rem" key={index}>
                        <TextInput
                            key={form.key(`messages.${index}`)}
                            flex={1}
                            {...form.getInputProps(`messages.${index}`)}
                        />
                        <ActionIcon
                            variant="subtle"
                            size="lg"
                            title="Remove message"
                            onClick={() =>
                                form.removeListItem('messages', index)
                            }
                        >
                            <IconX size={22} />
                        </ActionIcon>
                    </Flex>
                ))}

                <Flex>
                    <ActionIcon
                        variant="light"
                        size="lg"
                        onClick={() => form.insertListItem('messages', '')}
                        title="Add message"
                    >
                        <IconPlus size={22} />
                    </ActionIcon>
                </Flex>
            </Flex>
        </Flex>
    )
}

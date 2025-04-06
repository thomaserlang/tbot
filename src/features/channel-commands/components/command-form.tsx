import { accessLevelLabels } from '@/types/access-level.type'
import { providerLabels } from '@/types/provider.type'
import {
    Anchor,
    Flex,
    NumberInput,
    Select,
    SimpleGrid,
    Switch,
    TagsInput,
    TextInput,
} from '@mantine/core'
import { UseFormReturnType } from '@mantine/form'
import {
    IconExclamationMark,
    IconHourglassEmpty,
    IconLineDotted,
    IconLock,
    IconMessage,
} from '@tabler/icons-react'
import {
    commandActiveModeLabels,
    CommandCreate,
    CommandUpdate,
} from '../command.types'

interface Props {
    form: UseFormReturnType<CommandCreate> | UseFormReturnType<CommandUpdate>
}

export function CommandForm({ form }: Props) {
    return (
        <Flex direction="column" gap="1rem">
            <TagsInput
                leftSection={<IconExclamationMark size={16} />}
                label="Command triggers"
                placeholder="Type and press enter"
                key={form.key('cmds')}
                onKeyDown={(event) => {
                    if (event.key === '!') {
                        event.preventDefault()
                    }
                    if (event.key === ' ') {
                        event.preventDefault()
                    }
                }}
                {...form.getInputProps('cmds')}
            />

            <TagsInput
                leftSection={<IconLineDotted size={16} />}
                label="Command patterns"
                placeholder="Type and press enter"
                key={form.key('patterns')}
                onKeyDown={(event) => {
                    if (event.key === '!') {
                        event.preventDefault()
                    }
                }}
                {...form.getInputProps('patterns')}
            />

            <TextInput
                leftSection={<IconMessage size={16} />}
                label={
                    <>
                        Response{' '}
                        <Anchor
                            href="https://docs.botashell.com"
                            target="_blank"
                            size="sm"
                        >
                            (Variable docs)
                        </Anchor>
                    </>
                }
                key={form.key('response')}
                {...form.getInputProps('response')}
            />

            <SimpleGrid cols={{ base: 2, md: 3 }}>
                <Select
                    leftSection={<IconLock size={16} />}
                    label="Access level"
                    key={form.key('access_level')}
                    data={Object.keys(accessLevelLabels).map((key) => ({
                        value: key,
                        label: accessLevelLabels[key],
                    }))}
                    {...form.getInputProps('access_level')}
                    defaultValue={form.values.access_level?.toString()}
                />

                <Select
                    label="Active when"
                    key={form.key('active_mode')}
                    data={Object.keys(commandActiveModeLabels).map((key) => ({
                        value: key,
                        label: commandActiveModeLabels[key],
                    }))}
                    {...form.getInputProps('active_mode')}
                />

                <TextInput
                    label="Group"
                    key={form.key('group_name')}
                    {...form.getInputProps('group_name')}
                />
            </SimpleGrid>

            <SimpleGrid cols={{ base: 2, md: 3 }}>
                <NumberInput
                    leftSection={<IconHourglassEmpty size={16} />}
                    label="Global cooldown"
                    key={form.key('global_cooldown')}
                    allowNegative={false}
                    suffix=" secs"
                    {...form.getInputProps('global_cooldown')}
                />

                <NumberInput
                    leftSection={<IconHourglassEmpty size={16} />}
                    label="Chatter cooldown"
                    key={form.key('chatter_cooldown')}
                    allowNegative={false}
                    suffix=" secs"
                    {...form.getInputProps('chatter_cooldown')}
                />

                <NumberInput
                    leftSection={<IconHourglassEmpty size={16} />}
                    label="Mod cooldown"
                    key={form.key('mod_cooldown')}
                    allowNegative={false}
                    suffix=" secs"
                    {...form.getInputProps('mod_cooldown')}
                />
            </SimpleGrid>

            <SimpleGrid cols={{ base: 2, md: 3 }}>
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
            <Flex>
                <Switch
                    label="Public"
                    description="Shown on the public commands page"
                    key={form.key('public')}
                    style={{ cursor: 'pointer' }}
                    {...form.getInputProps('public', { type: 'checkbox' })}
                />
            </Flex>
        </Flex>
    )
}

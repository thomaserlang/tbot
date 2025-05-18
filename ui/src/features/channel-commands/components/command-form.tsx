import { accessLevelInfo, providerInfo } from '@/constants'
import {
    Anchor,
    Flex,
    NumberInput,
    Select,
    SimpleGrid,
    Switch,
    TagsInput,
    Text,
    Textarea,
    TextInput,
} from '@mantine/core'
import { UseFormReturnType } from '@mantine/form'
import {
    IconExclamationMark,
    IconHourglassEmpty,
    IconLineDotted,
    IconLock,
} from '@tabler/icons-react'
import {
    commandActiveModeLabels,
    CommandCreate,
    CommandUpdate,
} from '../types/command.types'

interface Props {
    form: UseFormReturnType<CommandCreate> | UseFormReturnType<CommandUpdate>
}

export function CommandForm({ form }: Props) {
    return (
        <Flex direction="column" gap="1rem">
            <TagsInput
                leftSection={<IconExclamationMark size={16} />}
                label="Command triggers"
                description="Write the commands without the !."
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
                label="Phrase triggers"
                description="The command will be triggered when the phrase is detected in a message. Use the prefix `re:` for a regular expression."
                placeholder="Type and press enter"
                key={form.key('patterns')}
                onKeyDown={(event) => {
                    if (event.key === '!') {
                        event.preventDefault()
                    }
                }}
                {...form.getInputProps('patterns')}
            />

            <Flex gap="0.10rem" direction="column">
                <Textarea
                    label={
                        <>
                            Response{' '}
                            <Anchor
                                target="_blank"
                                href="https://docs.synchra.net/cmd-vars"
                                size="sm"
                            >
                                (help)
                            </Anchor>
                        </>
                    }
                    autosize
                    minRows={3}
                    minLength={1}
                    maxLength={400}
                    w="100%"
                    key={form.key('response')}
                    {...form.getInputProps('response')}
                />
                <Text size="sm" c="dimmed" ml="auto">
                    {form.values.response?.length}/400
                </Text>
            </Flex>

            <SimpleGrid cols={{ base: 2, md: 3 }}>
                <Select
                    leftSection={<IconLock size={16} />}
                    label="Access level"
                    key={form.key('access_level')}
                    data={Object.values(accessLevelInfo).map((accessLevel) => ({
                        value: accessLevel.value.toString(),
                        label: accessLevel.label,
                    }))}
                    {...form.getInputProps('access_level')}
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
                    data={Object.values({
                        all: { key: 'all', name: 'All', chat_write: true },
                        ...providerInfo,
                    })
                        .filter((t) => t.chat_write)
                        .map((value) => ({
                            value: value.key,
                            label: value.name,
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

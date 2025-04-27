import { setFormErrors } from '@/utils/form'
import { toastError, toastSuccess } from '@/utils/toast'
import {
    Button,
    Flex,
    NumberInput,
    SimpleGrid,
    Switch,
    TagsInput,
    TextInput,
} from '@mantine/core'
import { useForm } from '@mantine/form'
import { useUpdateChannelPointSettings } from '../api/channel-point-settings.api'
import { ChannelPointSettings } from '../types/channel-point-settings.type'

interface Props {
    settings: ChannelPointSettings
}

export function ChannelPointSettingsForm({ settings }: Props) {
    const form = useForm({
        initialValues: {
            ...settings,
            channel_id: undefined,
        },
    })
    const update = useUpdateChannelPointSettings({
        onSuccess: () => {
            toastSuccess('Point settings updated')
        },
        onError: (error) => {
            toastError(error)
            if (error.status === 422) setFormErrors(form, error.response.data)
        },
    })

    return (
        <form
            onSubmit={form.onSubmit((values) => {
                update.mutate({
                    channelId: settings.channel_id,
                    data: values,
                })
            })}
        >
            <Flex direction="column" gap="1rem">
                <Switch
                    label="Enabled"
                    key={form.key('enabled')}
                    {...form.getInputProps('enabled', { type: 'checkbox' })}
                />

                <SimpleGrid cols={2}>
                    <TextInput
                        label="Points Name"
                        key={form.key('points_name')}
                        {...form.getInputProps('points_name')}
                    />
                </SimpleGrid>

                <SimpleGrid cols={2}>
                    <NumberInput
                        label="Points per Minute"
                        min={0}
                        key={form.key('points_per_min')}
                        {...form.getInputProps('points_per_min')}
                    />

                    <NumberInput
                        label="Sub Multiplier"
                        key={form.key('points_per_min_sub_multiplier')}
                        {...form.getInputProps('points_per_min_sub_multiplier')}
                        min={0}
                        max={10}
                    />

                    <NumberInput
                        label="Points per Sub"
                        min={0}
                        key={form.key('points_per_sub')}
                        {...form.getInputProps('points_per_sub')}
                    />

                    <NumberInput
                        min={0}
                        label="Points per Cheer"
                        key={form.key('points_per_cheer')}
                        {...form.getInputProps('points_per_cheer')}
                    />
                </SimpleGrid>

                <TagsInput
                    label="Ignore Users"
                    key={form.key('ignore_users')}
                    {...form.getInputProps('ignore_users')}
                />

                <Flex>
                    <Button loading={update.isPending} ml="auto" type="submit">
                        Save
                    </Button>
                </Flex>
            </Flex>
        </form>
    )
}

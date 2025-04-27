import { setFormErrors } from '@/utils/form'
import { toastError, toastSuccess } from '@/utils/toast'
import { Button, Flex, NumberInput, SimpleGrid, Textarea } from '@mantine/core'
import { useForm } from '@mantine/form'
import { useUpdateRouletteSettings } from '../api/roulette-settings.api'
import { RouletteSettings } from '../types/roulette-settings.type'

interface Props {
    settings: RouletteSettings
}

export function RouletteSettingsForm({ settings }: Props) {
    const form = useForm({
        initialValues: {
            ...settings,
            channel_id: undefined,
        },
    })
    const update = useUpdateRouletteSettings({
        onSuccess: () => {
            toastSuccess('Roulette settings saved')
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
                <SimpleGrid cols={{ base: 2, sm: 3 }}>
                    <NumberInput
                        label="Win chance"
                        min={0}
                        max={100}
                        key={form.key('win_chance')}
                        {...form.getInputProps('win_chance')}
                    />
                    <NumberInput
                        label="Minimum bet"
                        min={0}
                        key={form.key('min_bet')}
                        {...form.getInputProps('min_bet')}
                    />

                    <NumberInput
                        label="Maximum bet"
                        key={form.key('max_bet')}
                        {...form.getInputProps('max_bet')}
                        min={0}
                        max={10}
                    />
                </SimpleGrid>

                <SimpleGrid cols={1}>
                    <Textarea
                        label="Win message"
                        key={form.key('win_message')}
                        {...form.getInputProps('win_message')}
                    />

                    <Textarea
                        label="Lose message"
                        key={form.key('lose_message')}
                        {...form.getInputProps('lose_message')}
                    />

                    <Textarea
                        label="All in win message"
                        key={form.key('allin_win_message')}
                        {...form.getInputProps('allin_win_message')}
                    />

                    <Textarea
                        label="All in lose message"
                        key={form.key('allin_lose_message')}
                        {...form.getInputProps('allin_lose_message')}
                    />
                </SimpleGrid>

                <Flex>
                    <Button loading={update.isPending} ml="auto" type="submit">
                        Save
                    </Button>
                </Flex>
            </Flex>
        </form>
    )
}

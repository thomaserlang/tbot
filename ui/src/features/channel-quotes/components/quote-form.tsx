import { providerInfo } from '@/constants/providers-info.constants'
import { Flex, Select, SimpleGrid, Textarea, TextInput } from '@mantine/core'
import { UseFormReturnType } from '@mantine/form'
import { ChannelQuoteCreate, ChannelQuoteUpdate } from '../types/quote.types'

interface Props {
    form:
        | UseFormReturnType<ChannelQuoteCreate>
        | UseFormReturnType<ChannelQuoteUpdate>
}

export function QuoteForm({ form }: Props) {
    return (
        <Flex direction="column" gap="1rem">
            <SimpleGrid cols={2}>
                <TextInput
                    label="Created by"
                    placeholder="Name"
                    key={form.key('created_by_display_name')}
                    {...form.getInputProps('created_by_display_name')}
                />
                <TextInput
                    label="Created by ID"
                    placeholder="Viewer ID"
                    key={form.key('created_by_provider_viewer_id')}
                    {...form.getInputProps('created_by_provider_viewer_id')}
                />
            </SimpleGrid>

            <SimpleGrid cols={2}>
                <Select
                    label="Provider"
                    key={form.key('provider')}
                    {...form.getInputProps('provider')}
                    data={Object.values(providerInfo).map((p) => ({
                        value: p.key,
                        label: p.name,
                    }))}
                />
            </SimpleGrid>

            <Textarea
                label="Quote"
                key={form.key('message')}
                {...form.getInputProps('message')}
                autosize
            />
        </Flex>
    )
}

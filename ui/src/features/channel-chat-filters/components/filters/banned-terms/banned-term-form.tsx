import { Flex, Select, TextInput } from '@mantine/core'
import { UseFormReturnType } from '@mantine/form'
import { BannedTermRequest, bannedTermTypeLabels } from './banned-terms.types'

interface Props {
    form: UseFormReturnType<BannedTermRequest>
}

export function BannedTermForm({ form }: Props) {
    return (
        <Flex direction="column" gap="1rem">
            <Flex>
                <Select
                    label="Type"
                    data={Object.keys(bannedTermTypeLabels).map((key) => ({
                        value: key,
                        label: bannedTermTypeLabels[key],
                    }))}
                    key={form.key('type')}
                    {...form.getInputProps('type')}
                />
            </Flex>

            <TextInput
                label="Text"
                key={form.key('text')}
                {...form.getInputProps('text')}
            />
        </Flex>
    )
}

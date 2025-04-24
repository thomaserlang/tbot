import { Box, Flex, Tabs, TextInput } from '@mantine/core'
import { useForm } from '@mantine/form'
import { IconBan, IconSettings } from '@tabler/icons-react'
import { useState } from 'react'
import { filterToBaseRequest } from '../../../filter-utils'
import {
    ChatFilterBase,
    ChatFilterMatchResult,
    ChatFilterRequestBase,
} from '../../../filter.types'
import { EditFilterForm } from '../../filter-edit-form'
import { EditFilterProps } from '../edit-filter.types'
import { BannedTermsTable } from './banned-terms-table'
import { BannedTermsTest } from './banned-terms-test'
import { BannedTermId } from './banned-terms.types'
import { CreateBannedTermButton } from './create-banned-term-button'

export interface ChatFilterBannedTermsRequest extends ChatFilterRequestBase {
    type: 'banned_terms'
}
export interface ChatFilterBannedTerms extends ChatFilterBase {
    type: 'banned_terms'
}

export function EditBannedTermsFilter(
    props: EditFilterProps<ChatFilterBannedTerms>
) {
    const [matchTest, setMatchSet] = useState<ChatFilterMatchResult | null>(
        null
    )
    const form = useForm<ChatFilterBannedTermsRequest>({
        mode: 'uncontrolled',
        initialValues: {
            ...filterToBaseRequest(props.filter),
            type: props.filter.type,
        },
    })

    return (
        <Tabs defaultValue="settings">
            <Tabs.List mb="0.5rem">
                <Tabs.Tab
                    value="settings"
                    leftSection={<IconSettings size={12} />}
                >
                    Settings
                </Tabs.Tab>
                <Tabs.Tab
                    value="banned_terms"
                    leftSection={<IconBan size={12} />}
                >
                    Banned Terms
                </Tabs.Tab>
            </Tabs.List>

            <Tabs.Panel value="settings">
                <EditFilterForm {...props} form={form}>
                    <TextInput
                        label="Name"
                        key={form.key('name')}
                        {...form.getInputProps('name')}
                    />
                </EditFilterForm>
            </Tabs.Panel>

            <Tabs.Panel value="banned_terms">
                <Flex direction="column" h="30rem" gap="0.5rem">
                    <Flex wrap="wrap" gap="0.5rem">
                        <Flex>
                            <BannedTermsTest
                                channelId={props.filter.channel_id}
                                chatFilterId={props.filter.id}
                                onChange={setMatchSet}
                                value={matchTest}
                            />
                        </Flex>
                        <Box ml="auto">
                            <CreateBannedTermButton
                                channelId={props.filter.channel_id}
                                chatFilterId={props.filter.id}
                                onCreated={() => {
                                    setMatchSet(null)
                                }}
                            />
                        </Box>
                    </Flex>
                    <BannedTermsTable
                        channelId={props.filter.channel_id}
                        chatFilterId={props.filter.id}
                        selectedId={matchTest?.sub_id as BannedTermId}
                        onUpdated={() => {
                            setMatchSet(null)
                        }}
                    />
                </Flex>
            </Tabs.Panel>
        </Tabs>
    )
}

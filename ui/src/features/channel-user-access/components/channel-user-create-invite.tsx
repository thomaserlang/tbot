import { accessLevelInfo } from '@/constants/access-levels-info.constants'
import { ChannelId } from '@/features/channel/types/channel.types'
import { AccessLevel } from '@/types/access-level.type'
import { toastError } from '@/utils/toast'
import { Button, CopyButton, Flex, Select, TextInput } from '@mantine/core'
import { useForm } from '@mantine/form'
import { useCreateChannelUserInvite } from '../api/channel-user-invite.api'

interface Props {
    channelId: ChannelId
}

export function ChannelUserCreateInvite({ channelId }: Props) {
    const form = useForm({
        initialValues: {
            access_level: AccessLevel.MOD.toString(),
        },
    })
    const create = useCreateChannelUserInvite({
        onError: (error) => {
            toastError(error)
        },
    })

    return (
        <Flex gap="1rem" direction="column">
            {!create.data && (
                <form
                    onSubmit={form.onSubmit((values) => {
                        create.mutate({
                            channelId,
                            data: {
                                access_level: parseInt(values.access_level),
                            },
                        })
                    })}
                >
                    <Flex gap="0.5rem" align="end">
                        <Select
                            flex={1}
                            label="Access level"
                            data={Object.values(accessLevelInfo)
                                .filter(
                                    (accessLevel) =>
                                        accessLevel.value >= AccessLevel.MOD
                                )
                                .map((accessLevel) => ({
                                    value: accessLevel.value.toString(),
                                    label: accessLevel.label,
                                }))}
                            key={form.key('access_level')}
                            {...form.getInputProps('access_level')}
                        />
                        <Button loading={create.isPending} type="submit">
                            Create invite link
                        </Button>
                    </Flex>
                </form>
            )}

            {create.data && (
                <Flex gap="0.5rem" align="center">
                    <TextInput
                        flex={1}
                        value={create.data.invite_link}
                        readOnly
                        onClick={(e) => {
                            e.currentTarget.select()
                        }}
                    />
                    <CopyButton value={create.data.invite_link}>
                        {({ copied, copy }) => (
                            <Button
                                color={copied ? 'teal' : 'blue'}
                                onClick={copy}
                            >
                                {copied ? 'Copied url' : 'Copy url'}
                            </Button>
                        )}
                    </CopyButton>
                </Flex>
            )}
        </Flex>
    )
}

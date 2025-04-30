import { Flex, Text, Textarea, TextareaProps } from '@mantine/core'
import { useRef } from 'react'

interface Props extends TextareaProps {}

export function TextareaLimitIndicator(props: Props) {
    const ref = useRef<HTMLTextAreaElement>(null)
    return (
        <Flex gap="0.10rem" direction="column">
            <Textarea ref={ref} {...props} />
            <Text size="sm" c="dimmed" ml="auto">
                {ref.current?.value.length || props.value?.toString().length} /{' '}
                {props.maxLength || 0}
            </Text>
        </Flex>
    )
}

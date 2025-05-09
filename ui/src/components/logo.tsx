import { Anchor, Image, StyleProp } from '@mantine/core'
import logo from './logo.svg'

interface Props {
    width: StyleProp<React.CSSProperties['width']>
}
export function Logo({ width }: Props) {
    return (
        <Anchor href="/channels">
            <Image src={logo} alt="Synchra" w={width} />
        </Anchor>
    )
}

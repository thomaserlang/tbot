import { Anchor, Image } from '@mantine/core'
import logo from './logo.svg'

interface Props {
    width: string
}
export function Logo({ width }: Props) {
    return (
        <Anchor href="/">
            <Image
                src={logo}
                alt="HEIMRA"
                w={width}
                style={{ stroke: 'blue', color: 'blue' }}
            />
        </Anchor>
    )
}

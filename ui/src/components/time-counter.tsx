import { timeSinceStart } from '@/utils/date'
import { useInterval } from '@mantine/hooks'
import { useEffect, useState } from 'react'

interface Props {
    fromDateTime: string
}

export function TimeCounter({ fromDateTime }: Props) {
    const [time, setTime] = useState(timeSinceStart(fromDateTime))
    const interval = useInterval(
        () => setTime(() => timeSinceStart(fromDateTime)),
        1000
    )

    useEffect(() => {
        interval.start()
        return interval.stop
    }, [])

    return time
}

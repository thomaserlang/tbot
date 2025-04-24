import { dateToRelativeTime } from '@/utils/date'
import { useInterval } from '@mantine/hooks'
import { useEffect, useState } from 'react'

interface Props {
    dt: string
}

export function RelativeTimeUpdater({ dt }: Props) {
    const [time, setTime] = useState(dateToRelativeTime(dt))
    const interval = useInterval(
        () => setTime(() => dateToRelativeTime(dt)),
        1000
    )

    useEffect(() => {
        interval.start()
        return interval.stop
    }, [])

    return time
}

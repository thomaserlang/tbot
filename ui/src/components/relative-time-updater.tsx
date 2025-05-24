import { dateToRelativeTime, dateToShortRelativeTime } from '@/utils/date'
import { useEffect, useState } from 'react'

interface Props {
    date: string
}

export function RelativeTimeUpdater({ date }: Props) {
    const [time, setTime] = useState(dateToRelativeTime(date))
    useEffect(() => {
        const interval = setInterval(() => {
            setTime(() => dateToRelativeTime(date))
        }, 1000)
        return () => clearInterval(interval)
    }, [date])

    return time
}

export function ShortRelativeTimeUpdater({ date }: Props) {
    const [time, setTime] = useState(dateToShortRelativeTime(date))

    useEffect(() => {
        const interval = setInterval(() => {
            setTime(() => dateToShortRelativeTime(date))
        }, 60000)

        return () => clearInterval(interval)
    }, [date])

    return time
}

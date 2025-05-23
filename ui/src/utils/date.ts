import dayjs from 'dayjs'
import localizedFormat from 'dayjs/plugin/localizedFormat'
import relativeTime from 'dayjs/plugin/relativeTime'
dayjs.extend(localizedFormat)
dayjs.extend(relativeTime)

export function strDateFormat(date: string | Date): string {
    if (!date) return ''

    return dayjs(date).format('LL')
}

export function timeSinceStart(startDateTime: string | Date): string {
    if (!startDateTime) return ''

    const duration = dayjs().diff(startDateTime, 'second')
    const hours = Math.floor(duration / 3600)
    const minutes = Math.floor((duration % 3600) / 60)
    const seconds = duration % 60

    return `${hours.toString().padStart(1, '0')}:${minutes
        .toString()
        .padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
}

export function dateToRelativeTime(date: string | Date): string {
    return dayjs(date).fromNow(true)
}

export function dateToShortRelativeTime(date: string | Date): string {
    const now = dayjs()
    const then = dayjs(date)

    const diffSec = now.diff(then, 'second')

    if (diffSec < 60) {
        return `Now`
    }

    const diffMin = Math.floor(diffSec / 60)
    if (diffMin < 60) {
        return `${diffMin}m`
    }

    const diffHour = Math.floor(diffMin / 60)
    if (diffHour < 24) {
        return `${diffHour}h`
    }

    const diffDay = Math.floor(diffHour / 24)
    return `${diffDay}d`
}

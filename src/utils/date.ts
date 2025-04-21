import dayjs from 'dayjs'
import localizedFormat from 'dayjs/plugin/localizedFormat'
dayjs.extend(localizedFormat)

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

    return `${hours.toString().padStart(2, '0')}:${minutes
        .toString()
        .padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
}

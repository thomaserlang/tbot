import dayjs from 'dayjs'
import localizedFormat from 'dayjs/plugin/localizedFormat'
dayjs.extend(localizedFormat)

export function strDateFormat(date: string | Date): string {
    if (!date) return ''

    return dayjs(date).format('LL')
}

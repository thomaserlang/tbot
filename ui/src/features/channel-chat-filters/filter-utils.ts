import { ChatFilter } from './filter-registry'
import { ChatFilterRequestBase } from './filter.types'

export function filterToBaseRequest(filter: ChatFilter): ChatFilterRequestBase {
    return {
        name: filter.name,
        type: filter.type,
        provider: filter.provider,
        enabled: filter.enabled,
        exclude_access_level: filter.exclude_access_level.toString(),
        warning_enabled: filter.warning_enabled,
        warning_message: filter.warning_message,
        warning_expire_duration: filter.warning_expire_duration,
        timeout_message: filter.timeout_message,
        timeout_duration: filter.timeout_duration,
    }
}

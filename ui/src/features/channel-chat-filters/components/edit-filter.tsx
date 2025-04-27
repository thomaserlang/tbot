import { ChatFilter, registeredFilters } from '../filter-registry'

interface Props {
    filter: ChatFilter
    onUpdated?: (filter: ChatFilter) => void
}

export function EditFilter(props: Props) {
    const Component = registeredFilters[props.filter.type].component

    return <Component {...(props as any)} /> // TODO: how to type this properly?
}

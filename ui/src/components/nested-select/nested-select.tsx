import {
    IListGroupedItem,
    IListToGroupsItem,
    listToGroups,
} from '@/utils/group-data'
import { Flex } from '@mantine/core'
import { IconChevronRight } from '@tabler/icons-react'
import clsx from 'clsx'
import { ContextMenuContent, useContextMenu } from 'mantine-contextmenu'
import { DataTable, DataTableRowClickHandler } from 'mantine-datatable'
import { Dispatch, SetStateAction, useEffect, useState } from 'react'
import { SelectNestedSearch } from './nested-select-search'
import classes from './nested-select.module.css'

interface Props<T = any> {
    data: IListToGroupsItem<T>[]
    isLoading?: boolean
    defaultValue?: string
    noRecordsText?: string
    onRowContextMenu?: (item: T) => ContextMenuContent
    onSelect?: (item: T) => void
    titleExtraContent?: (item: IListGroupedItem<T>) => React.ReactNode
    extraContent?: (item: IListGroupedItem<T>) => React.ReactNode
}

export function NestedSelect<T = any>({
    data,
    isLoading,
    defaultValue,
    noRecordsText,
    onRowContextMenu,
    onSelect,
    titleExtraContent,
    extraContent,
}: Props<T>) {
    const { showContextMenu } = useContextMenu()
    const [expandedIds, setExpandedIds] = useState<string[]>([])
    const [grouped, setGrouped] = useState<IListGroupedItem<T>[]>(
        listToGroups(data)
    )

    useEffect(() => {
        const d = listToGroups(data)
        setGrouped(d)
        if (defaultValue) {
            setExpandedIds(expandSelectedItemValue(d, defaultValue))
            scrollRowIntoView(`[data-row-value="${btoa(defaultValue)}"]`)
        }
    }, [data, defaultValue])

    return (
        <Flex direction="column" gap="0.5rem" h="100%">
            <SelectNestedSearch
                data={data}
                onResults={(results) => {
                    const grouped = listToGroups(results)
                    setGrouped(grouped)
                    if (results.length === data.length) setExpandedIds([])
                    else if (results.length <= 50)
                        setExpandedIds(expandAll(grouped))
                }}
            />

            <Table
                data={grouped}
                nestedLevel={0}
                expandedIds={expandedIds}
                setExpandedIds={setExpandedIds}
                onSelect={onSelect}
                titleExtraContent={titleExtraContent}
                extraContent={extraContent}
                isLoading={isLoading}
                noRecordsText={noRecordsText}
                onRowContextMenu={({ record, event }) =>
                    onRowContextMenu &&
                    record.object &&
                    showContextMenu(onRowContextMenu(record.object), {
                        styles: {
                            item: { minWidth: 200 },
                        },
                    })(event)
                }
            />
        </Flex>
    )
}

interface TableProps<T = any> {
    isLoading?: boolean
    data: IListGroupedItem<T>[]
    nestedLevel: number
    expandedIds: string[]
    noRecordsText?: string
    onRowContextMenu: DataTableRowClickHandler<IListGroupedItem<T>>
    setExpandedIds: Dispatch<SetStateAction<string[]>>
    onSelect?: (item: T) => void
    titleExtraContent?: (item: IListGroupedItem<T>) => React.ReactNode
    extraContent?: (item: IListGroupedItem<T>) => React.ReactNode
}

function Table<T = any>(props: TableProps<T>) {
    return (
        <DataTable
            idAccessor="value"
            highlightOnHover
            noHeader
            withTableBorder={props.nestedLevel === 0}
            withColumnBorders={props.nestedLevel === 0}
            fetching={props.isLoading}
            noRecordsText={props.noRecordsText}
            onRowContextMenu={props.onRowContextMenu}
            records={props.data}
            customRowAttributes={({ value }) => ({
                'data-row-value': btoa(value),
            })}
            rowClassName="pointer"
            columns={[
                {
                    accessor: 'name',
                    noWrap: true,
                    render: (record) => (
                        <Flex
                            direction="column"
                            gap="0.25rem"
                            pl={props.nestedLevel * 10}
                            w="100%"
                        >
                            <Flex align="center">
                                {record.items && (
                                    <IconChevronRight
                                        className={clsx(
                                            classes.icon,
                                            classes.expandIcon,
                                            {
                                                [classes.expandIconRotated]:
                                                    props.expandedIds.includes(
                                                        record.value
                                                    ),
                                            }
                                        )}
                                    />
                                )}
                                <Flex gap="1rem" w="100%" align="center">
                                    <span>{record.name}</span>
                                    {props.titleExtraContent?.(record)}
                                </Flex>
                            </Flex>
                            {props.extraContent?.(record)}
                        </Flex>
                    ),
                },
            ]}
            onRowClick={({ record }) => {
                if (record.object) {
                    props.onSelect?.(record.object)

                    props.setExpandedIds((prev) => {
                        if (prev.includes(record.value)) {
                            return prev.filter((id) => id !== record.value)
                        }
                        return [...prev, record.value]
                    })
                } else {
                    scrollRowIntoView(
                        `[data-row-value="${btoa(record.value)}"]`
                    )
                }
            }}
            rowExpansion={{
                allowMultiple: true,
                collapseProps: {
                    transitionDuration: 0,
                },
                expanded: {
                    recordIds: props.expandedIds,
                    onRecordIdsChange: (ids: SetStateAction<string[]>) => {
                        props.setExpandedIds(ids)
                    },
                },
                content: ({ record }) =>
                    record.items && (
                        <Table<T>
                            {...props}
                            nestedLevel={props.nestedLevel + 1}
                            data={record.items}
                        />
                    ),
            }}
        />
    )
}

function scrollRowIntoView(selector: string) {
    setTimeout(() => {
        document
            .querySelector(selector)
            ?.scrollIntoView({ block: 'center', behavior: 'auto' })
    }, 50) // wait for row to expand
}

function expandAll<T>(grouped: IListGroupedItem<T>[]) {
    const values: string[] = []
    function collectIds(items: IListGroupedItem<T>[]) {
        for (const item of items) {
            if (item.items) {
                values.push(item.value)
                collectIds(item.items)
            }
        }
    }
    collectIds(grouped)
    return values
}

function expandSelectedItemValue<T>(
    grouped: IListGroupedItem<T>[],
    selectedValue: string
) {
    const values: string[] = []
    function collectIds(items: IListGroupedItem<T>[]) {
        for (const item of items) {
            if (item.value === selectedValue) {
                values.push(item.value)
                return true
            }
            if (item.items && collectIds(item.items)) {
                values.push(item.value)
                return true
            }
        }
        return false
    }
    collectIds(grouped)
    return values
}

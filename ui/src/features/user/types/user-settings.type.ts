export interface UserSettings {
    activity_feed_not_types: string[]
    activity_feed_type_min_count: { [activityType: string]: number }
    activity_feed_read_indicator: boolean
}

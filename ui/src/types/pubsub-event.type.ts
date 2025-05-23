export interface PubSubEvent<DataT> {
    type: 'activity' | 'chat_message'
    action: 'new' | 'updated' | 'deleted'
    data: DataT
}

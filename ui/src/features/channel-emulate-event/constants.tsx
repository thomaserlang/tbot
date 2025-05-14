import { api } from '@/utils/api'
import { EmulateEvent } from './types'

export const EmulateEvents: EmulateEvent[] = [
    {
        name: 'Redeem custom reward: waste points',
        request: ({ channelId }) => {
            return api.post(
                `/api/2/twitch/eventsub/emulate-custom-reward-redemption`,
                {
                    reward_title: 'Waste points',
                    reword_cost: 100,
                },
                {
                    params: {
                        channel_id: channelId,
                    },
                }
            )
        },
    },
    {
        name: 'Redeem custom reward: message',
        request: ({ channelId }) => {
            return api.post(
                `/api/2/twitch/eventsub/emulate-custom-reward-redemption`,
                {
                    reward_title: 'Message',
                    reward_cost: 100,
                    user_input: 'Test message 123...',
                },
                {
                    params: {
                        channel_id: channelId,
                    },
                }
            )
        },
    },
]

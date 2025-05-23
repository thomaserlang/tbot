import { api } from '@/utils/api'
import { EmulateEvent } from './types'

export const emulateEvents: EmulateEvent[] = [
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

    {
        name: 'Power up gigantify emote',
        request: ({ channelId }) => {
            return api.post(
                `/api/2/twitch/eventsub/emulate-channel-chat-message`,
                {
                    message_type: 'power_ups_gigantified_emote',
                    fragments: [
                        {
                            type: 'emote',
                            text: 'bahHappy',
                            cheermote: null,
                            emote: {
                                id: '873540',
                                emote_set_id: '33404',
                                owner_id: '77256527',
                                format: ['static'],
                            },
                            mention: null,
                        },
                        {
                            type: 'text',
                            text: ' test  ',
                            cheermote: null,
                            emote: null,
                            mention: null,
                        },
                        {
                            type: 'emote',
                            text: 'bahRat',
                            cheermote: null,
                            emote: {
                                id: 'emotesv2_b8c288d7d202433aaaf25bae6ad79ac3',
                                emote_set_id: '49155',
                                owner_id: '77256527',
                                format: ['static'],
                            },
                            mention: null,
                        },
                    ],
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
        name: 'Power up message effect',
        request: ({ channelId }) => {
            return api.post(
                `/api/2/twitch/eventsub/emulate-channel-chat-message`,
                {
                    message_type: 'power_ups_message_effect',
                    fragments: [
                        {
                            type: 'text',
                            text: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
                            cheermote: null,
                            emote: null,
                            mention: null,
                        },
                    ],
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
        name: 'Highlight message',
        request: ({ channelId }) => {
            return api.post(
                `/api/2/twitch/eventsub/emulate-channel-chat-message`,
                {
                    message_type: 'channel_points_highlighted',
                    fragments: [
                        {
                            type: 'text',
                            text: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
                            cheermote: null,
                            emote: null,
                            mention: null,
                        },
                    ],
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
        name: 'Celebration',
        request: ({ channelId }) => {
            return api.post(
                `/api/2/twitch/eventsub/emulate-automatic-reward-redemption`,
                {
                    reward_type: 'celebration',
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
        name: 'Subscription',
        request: ({ channelId }) => {
            return api.post(
                `/api/2/twitch/eventsub/emulate-subscription`,
                {},
                {
                    params: {
                        channel_id: channelId,
                    },
                }
            )
        },
    },

    {
        name: 'Cheer',
        request: ({ channelId }) => {
            return Promise.all([
                api.post(
                    '/api/2/twitch/eventsub/emulate-cheer',
                    { bits: 101051 },
                    {
                        params: {
                            channel_id: channelId,
                        },
                    }
                ),
                api.post(
                    `/api/2/twitch/eventsub/emulate-channel-chat-message`,
                    {
                        message_type: 'text',
                        fragments: [
                            {
                                type: 'cheermote',
                                text: 'cheer100001',
                                cheermote: {
                                    prefix: 'cheer',
                                    bits: 100001,
                                    tier: 100000,
                                },
                            },
                            {
                                type: 'text',
                                text: ' test ',
                            },
                            {
                                type: 'emote',
                                text: 'bahRat',
                                emote: {
                                    id: 'emotesv2_b8c288d7d202433aaaf25bae6ad79ac3',
                                    emote_set_id: '49155',
                                    owner_id: '77256527',
                                    format: ['static'],
                                },
                            },
                            {
                                type: 'text',
                                text: ' ',
                            },
                            {
                                type: 'cheermote',
                                text: 'cheer1050',
                                cheermote: {
                                    prefix: 'cheer',
                                    bits: 1050,
                                    tier: 1000,
                                },
                            },
                        ],
                        cheer: {
                            bits: 101051,
                        },
                    },
                    {
                        params: {
                            channel_id: channelId,
                        },
                    }
                ),
            ])
        },
    },
]

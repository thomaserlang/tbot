from ..base import Api_handler

class Handler(Api_handler):

    async def get(self, channel_id: str):
        result = await self.db.fetchone('''
            select
                sum(points) as points
            from
                (
                    select
                        s.user_id,
                        ifnull(
                            l.points,
                            if(s.tier = '3000', 6, s.tier / 1000)
                        ) as points
                    from
                        twitch_subs s
                        left join (
                            select
                                user_id
                            FROM
                                twitch_sub_log
                            where
                                channel_id = %s
                                and created_at >= NOW() - interval 30 DAY
                                and (
                                    (tier = 'prime')
                                    or (is_gift = TRUE)
                                )
                            group by
                                user_id
                        ) p_or_g on (p_or_g.user_id = s.user_id)
                        left join (
                            select
                                user_id,
                                if(tier = '3000', 6, tier / 1000) as points
                            FROM
                                twitch_sub_log
                            where
                                channel_id = %s
                                and created_at >= DATE_FORMAT(NOW(), '%%Y-%%m-01 00:00:00')
                                and tier != 'prime'
                                and is_gift = FALSE
                        ) l on (l.user_id = s.user_id)
                    where
                        s.channel_id = %s
                        and s.user_id != s.channel_id
                        and (day(s.created_at) <= day(now()))
                        and s.is_gift = FALSE
                        and isnull(p_or_g.user_id)

                    UNION

                    select
                        l.user_id,
                        sum(if(l.tier = '3000', 6, l.tier / 1000)) as points
                    FROM
                        twitch_sub_log l
                        left join twitch_subs s on (
                            s.channel_id = l.channel_id
                            and s.user_id = l.user_id
                        )
                    where
                        l.channel_id = %s
                        and l.created_at >= DATE_FORMAT(NOW(), '%%Y-%%m-01 00:00:00')
                        and l.tier != 'prime'
                        and l.is_gift = FALSE
                        and isnull(s.channel_id)
                ) as s
            ''',
            (channel_id, channel_id, channel_id, channel_id)
        )
        self.write_object({
            'points': result['points']
        })
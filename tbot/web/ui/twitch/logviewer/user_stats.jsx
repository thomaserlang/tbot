import { useEffect, useState } from "react"

import api from 'tbot/twitch/api'
import { secondsToText } from 'tbot/utils'

export default function UserStats({ channelId, user }) {
    const [loading, setLoading] = useState(true)
    const [data, setData] = useState(null)
    const [error, setError] = useState(false)
    
    useEffect(() => {
        setData(true)
        api.get(`/api/twitch/channels/${channelId}/user-chatstats`, {params: {
            user: user,
        }}).then(r => {
            setLoading(r.data)
            setError(false)
        }).catch((e) => {
            console.log(e)
            setData(null)
            setError(true)
        }).finally(() => {
            setLoading(false)
        })
    }, [channelId, user])

    if (loading) 
        return <div className="userChatStats">
            <div className="spacing">
                <h3>{user}</h3>
                <div className="user">
                    Loading user data...
                </div>
            </div>
        </div>

    if (error)
        return <div className="userChatStats">
            <div className="spacing">
                <h3>{user}</h3>
                <div className="user">
                    Failed to load user data, try again.
                </div>
            </div>
        </div>

    if (!data)
        return <div className="userChatStats">
            <div className="spacing">
                <h3>{user}</h3>
                <div className="user">
                    Didn't find any channel stats for user.
                </div>
            </div>
        </div>


    return <div className="userChatStats">
        <div className="spacing">
            <h3>{user}</h3>
            <div className="user">
                <div><div><b>Messages:</b></div> <div>{data.chat_messages||0}</div></div>
                <div><div><b>Timeouts:</b></div> <div>{data.timeouts||0}</div></div>
                <div><div><b>Bans:</b></div> <div>{data.bans||0}</div></div>
                <div title="Number of watched streams"><div><b>Streams:</b></div> <div>{data.streams||0}</div></div>
                <div title="Streams watched in a row"><div><b>Stream streak:</b></div> <div>{renderStreak(data)}</div></div>
                <div title="Date of the latest stream watched"><div><b>Latest stream:</b></div> <div>{data.last_viewed_stream_date||'No data'}</div></div>
                <div title=""><div><b>Watch time:</b></div> <div>{secondsToText(data.watchtime||0)}</div></div>
            </div>
        </div>
    </div>
}

function renderStreak(data) {
    if (!data.streams_row_peak) 
        return 0
    if (data.streams_row == data.streams_row_peak) {
        return data.streams_row
    } else {
        return `${data.streams_row} (Peak: ${data.streams_row_peak} - ${data.streams_row_peak_date})`
    }
}
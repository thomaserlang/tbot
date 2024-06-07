import { useEffect, useState } from "react"

import api from 'tbot/twitch/api'
import { secondsToText, iso8601toLocalTime } from "../../utils"


export default function({ channelId, user }) {
    const [data, setData] = useState('')
    const [loading, setLoading] = useState(true)
    const [loadingMore, setLoadingMore] = useState(false)
    const [canLoadMore, setCanLoadMore] = useState(false)
    const [error, setError] = useState(false)

    useEffect(() => {
        setLoading(false)
        api.get(`/api/twitch/channels/${channelId}/user-streams-watched`, {params: {
            user: user,
        }}).then(r => {
            setData(r.data)
            setCanLoadMore(r.data.length > 4)
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
        return <div style={{marginTop: '1rem'}}><h3>Streams watched</h3> <div className="spacing">Loading streams watched...</div></div>
    
    if (error) 
        return <div style={{marginTop: '1rem'}}><h3>Streams watched</h3> <div className="spacing">Failed to load streams watched, try again.</div></div>

    if (!data || (data.length === 0))
        return <div style={{marginTop: '1rem'}}><h3>Streams watched</h3> <div className="spacing">Didn't find any streams watched for user.</div></div>

    const loadMore = (e) => {
        e.preventDefault()
        setLoadingMore(true)
        api.get(`/api/twitch/channels/${channelId}/user-streams-watched`, {params: {
            user: user,
            after_id: data.at(-1).started_at
        }}).then(r => {
            setData([...data, ...r.data])
            setCanLoadMore(r.data.length > 4)
            setError(false)
        }).catch((e) => {
            console.log(e)
            setError(true)
        }).finally(() => (
            setLoadingMore(false)
        ))
    }

    return <div style={{marginTop: '1rem'}}>
        <h3>Streams watched</h3>
        <table className="table table-dark table-sm table-hover">
            <thead>
                <tr>
                    <th className="fit-content">Stream date</th>
                    <th className="fit-content">Stream uptime</th>
                    <th>Watch time</th>
                </tr>
            </thead>
            <tbody>
                {data.map(s => (
                    <tr key={s.stream_id}>
                        <td 
                            dateTime={s.started_at}
                            className="fit-content"
                        >
                            {iso8601toLocalTime(s.started_at).substring(0, 10)}
                        </td>
                        <td className="fit-content">
                            {secondsToText(s.uptime|0)} 
                        </td>
                        <td>
                            {secondsToText(s.watchtime|0)} {percentageWatched(s)}
                        </td>
                    </tr>
                ))}
                {canLoadMore?
                    <tr><td colSpan="3" style={{textAlign: 'center'}}>
                        {loadingMore?
                            <div className="spinner-grow text-primary" role="status"></div>:
                            <a href="#" onClick={loadMore}>Load more streams</a>}
                        </td>
                    </tr>: null
                }
            </tbody>
        </table>
    </div>
}

function percentageWatched(stream) {
    if (!stream.uptime)
        return null
    if (stream.watchtime > stream.uptime)
        return 100
    const p = ((100 * stream.watchtime) / stream.uptime).toFixed(0)
    return `(${p}%)`
}
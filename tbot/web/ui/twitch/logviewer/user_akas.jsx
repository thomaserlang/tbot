import { useEffect, useState } from "react"

import api from 'tbot/twitch/api'

export default function({ channelId, user }) {
    const [data, setData] = useState('')
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(false)

    useEffect(() => {
        setLoading(false)
        api.get(`/api/twitch/channels/${channelId}/user-akas`, {params: {
            user: user,
        }}).then(r => {
            setData(r.data)
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
        return <div></div>
    
    if (error) 
        return <div></div>

    if (data?.length < 2)
        return <div></div>

    return <div style={{marginTop: '1rem'}}>
        <h3>AKAs</h3>
        <table className="table table-dark table-sm table-hover">
            <tbody>
                {data.map(s => (
                    <tr key={s.user}>
                        <td 
                            className="fit-content"
                        >
                            {s.user}
                        </td>
                    </tr>
                ))}
            </tbody>
        </table>
    </div>
}
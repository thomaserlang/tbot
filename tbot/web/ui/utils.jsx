import moment from 'moment'

export function setTitle(title) {
    document.title = `${title} | ${window.tbot.name}`
}

export function setHeader(title) {
    setTitle(title)
    document.getElementById('top-title').innerHTML = title
}

export function renderError(error) {
    if (!error)
        return null
    if (error.errors)
        return <div className="alert alert-danger" role="alert">
            <div className="mb-2"><b>Error:</b> {error.message}</div>
            {error.errors.map(e => (
                <div key={e.field}><b>{e.field}:</b> {e.message}</div>
            ))}
        </div>
    return <div className="alert alert-danger" role="alert">
        <div><b>Error:</b> {error.message}</div>
    </div>
}

export function iso8601toLocalTime(t) {
    return moment(t).format('YYYY-MM-DD HH:mm:ss')
}

export function secondsToText(seconds) {
    const hours = Math.floor(seconds / 60 / 60)
    const minutes = Math.floor(seconds / 60) - (hours * 60)

    let s = ''

    if (hours > 0)
        s += `${hours} hour${hours!=1?'s':''}`

    if (minutes > 0) {
        if (hours > 0)
            s += ' ' 
        s += `${minutes} minute${minutes!=1?'s':''}`
    }

    return s
}
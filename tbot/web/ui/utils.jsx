
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
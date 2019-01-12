export default (props) => {
    return <div className="d-flex flex-column text-center">
        <div>
            <div className="spinner-grow text-primary" role="status" style={{
                width: '5rem',
                height: '5rem',
            }}>
                <span className="sr-only">Loading...</span>
            </div>
        </div>
        <div className="mt-2">
            <h1>{props.text}</h1>
        </div>
    </div>
}
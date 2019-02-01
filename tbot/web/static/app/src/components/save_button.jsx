export default(props) => {
    if (props.isSaving)
        return <button className="btn btn-primary" type="button" disabled>
                <span className="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Saving...
            </button>
    return <button type="submit" className="btn btn-primary">{props.children}</button>
}
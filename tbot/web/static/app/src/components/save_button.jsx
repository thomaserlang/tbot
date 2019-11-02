export default(props) => {
    if (props.isSaving)
        return <button className="btn btn-primary" type="button" disabled>
                <span 
                    className="spinner-border spinner-border-sm" 
                    role="status" 
                    aria-hidden="true">
                </span> {props.savingText?props.savingText:'Saving...'}
            </button>
    if (props.isSaved)
        return <button type="submit" className="btn btn-success">
            {props.savedText?props.savedText:props.children}
        </button>
    if (props.hasError)
        return <button type="submit" className="btn btn-danger">
            {props.errorText?props.errorText:props.children}
        </button>

    return <button type="submit" className="btn btn-primary">{props.children}</button>
}
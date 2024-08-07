import React from 'react'
import {Redirect} from 'react-router'
import api from 'tbot/twitch/api'
import Loading from 'tbot/components/loading'
import {setHeader, renderError} from 'tbot/utils'
import {userLevelName, enabledWhenName} from 'tbot/twitch/utils'

class Quote extends React.Component {

    constructor(props) {
        super(props)
        this.state = {
            cmd: {
                message: '',
                date: '',
            },
            loading: true,
            error: null,
            saving: false,
            success: false,
        }
    }

    componentDidMount() {
        if (this.props.match.params.number) {
            setHeader('Edit quote')
            this.getQuote()
        } else {            
            setHeader('New quote')
            this.setState({loading: false})
        }
    }

    getQuote() {        
        const number = this.props.match.params.number
        api.get(`/api/twitch/channels/${managedUser.id}/quotes/${number}`).then(r => {
            for (let key in r.data) {
                if (!(key in this.state.cmd))
                    delete r.data[key]
            }
            this.setState({
                quote: r.data, 
                loading: false
            })
            setHeader(`Edit quote`)
        })
    }

    handleEvent = (e) => {
        let val = e.target.type === 'checkbox' ? e.target.checked : e.target.value
        this.state.quote[e.target.name] = val
        this.setState({quote: this.state.quote})
    }

    handleSubmit = (e) => {
        e.preventDefault()
        this.setState({saving: true, error: null})
        const number = this.props.match.params.number
        if (number)
            api.put(`/api/twitch/channels/${managedUser.id}/quotes/${number}`, this.state.quote).then(r => {
                this.setState({success: true})
            }).catch(e => {
                this.setState({error: e.response.data, saving: false})
            })
        else 
            api.post(`/api/twitch/channels/${managedUser.id}/quotes`, this.state.quote).then(r => {
                this.setState({success: true})
            }).catch(e => {
                this.setState({error: e.response.data, saving: false})
            })
    }

    handleDelete = () => {
        if (!confirm(`Delete quote?`))
            return
        this.setState({deleting: true, error: null})
        let number = this.props.match.params.number
        api.delete(`/api/twitch/channels/${managedUser.id}/quotes/${number}`).then(r => {
            this.setState({
                cmd: r.data, 
                success: true,
            })
        }).catch(e => {
            this.setState({error: e.response.data, deleting: false})
        })
    }

    renderButton() {
        if (this.state.saving)
            return <button className="btn btn-primary" type="button" disabled>
                    <span className="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Saving...
                </button>
        return <button type="submit" className="btn btn-primary">Save quote</button>
    }

    renderDeleteButton() {
        if (!this.props.match.params.number)
            return null
        if (this.state.deleting)
            return <button className="ml-2 btn btn-danger" type="button" disabled>
                    <span className="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Deleting...
                </button>
        return <button type="button" onClick={this.handleDelete} className="ml-2 btn btn-danger">Delete quote</button>
    }

    render() {
        if (this.state.loading)
            return <Loading />
        if (this.state.success)
            return <Redirect to={`/twitch/${this.props.match.params.channel}/quotes`} />

        return <div style={{maxWidth:'700px'}}>
            <form onSubmit={this.handleSubmit}>

            <div className="form-group">
                <input 
                    className="form-control" 
                    id="message" 
                    name="message" 
                    value={this.state.quote.message}
                    onChange={this.handleEvent}
                    required
                />
            </div>

            {renderError(this.state.error)}
            {this.renderButton()}
            {this.renderDeleteButton()}
        </form>
        </div>
    }
}

export default Quote
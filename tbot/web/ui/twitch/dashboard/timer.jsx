import React from 'react'
import {Redirect} from 'react-router'
import api from 'tbot/twitch/api'
import Loading from 'tbot/components/loading'
import {setHeader, renderError} from 'tbot/utils'
import {userLevelName, enabledWhenName} from 'tbot/twitch/utils'

class Timer extends React.Component {

    constructor(props) {
        super(props)
        this.state = {
            timer: {
                name: '',
                messages: '',
                enabled_status: 0,
                enabled: 1,
                interval: 5,
                send_message_order: 1,
            },
            loading: true,
            error: null,
            saving: false,
            success: false,
        }
    }

    componentDidMount() {
        if (this.props.match.params.id) {
            setHeader('Edit timer')
            this.getTimer()
        } else {            
            setHeader('New timer')
            this.setState({loading: false})
        }
    }

    getTimer() {        
        let id = this.props.match.params.id
        api.get(`/api/twitch/channels/${managedUser.id}/timers/${id}`).then(r => {
            for (let key in r.data) {
                if (!(key in this.state.timer))
                    delete r.data[key]
            }
            r.data.messages = r.data.messages.join('\n')
            this.setState({
                timer: r.data, 
                loading: false
            })
            setHeader(`Edit timer: ${r.data.name}`)
        })
    }

    handleEvent = (e) => {
        let val = e.target.type === 'checkbox' ? e.target.checked : e.target.value
        this.state.timer[e.target.name] = val
        this.setState({timer: this.state.timer})
    }

    handleSubmit = (e) => {
        e.preventDefault()
        this.setState({saving: true, error: null})
        if (!Array.isArray(this.state.timer.messages))
            this.state.timer.messages = this.state.timer.messages.split('\n')
        this.state.timer.messages = this.state.timer.messages.filter(e => (
            e != ''
        ))
        let id = this.props.match.params.id
        if (id)
            api.put(`/api/twitch/channels/${managedUser.id}/timers/${id}`, this.state.timer).then(r => {
                this.setState({success: true})
            }).catch(e => {
                this.state.timer.messages = this.state.timer.messages.join('\n')
                this.setState({error: e.response.data, saving: false})
            })
        else 
            api.post(`/api/twitch/channels/${managedUser.id}/timers`, this.state.timer).then(r => {
                this.setState({success: true})
            }).catch(e => {
                this.state.timer.messages = this.state.timer.messages.join('\n')
                this.setState({error: e.response.data, saving: false})
            })
    }

    handleDelete = () => {
        if (!confirm(`Delete timer: ${this.state.timer.timer}?`))
            return
        this.setState({deleting: true, error: null})
        let id = this.props.match.params.id
        api.delete(`/api/twitch/channels/${managedUser.id}/timers/${id}`).then(r => {
            this.setState({
                timer: r.data, 
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
        return <button type="submit" className="btn btn-primary">Save Timer</button>
    }

    renderDeleteButton() {
        if (!this.props.match.params.id)
            return null
        if (this.state.deleting)
            return <button className="ml-2 btn btn-danger" type="button" disabled>
                    <span className="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Deleting...
                </button>
        return <button type="button" onClick={this.handleDelete} className="ml-2 btn btn-danger">Delete Timer</button>
    }

    render() {
        if (this.state.loading)
            return <Loading />
        if (this.state.success)
            return <Redirect to={`/twitch/${this.props.match.params.channel}/timers`} />

        return <form onSubmit={this.handleSubmit} style={{maxWidth:'700px'}}>
            <div className="form-group">
                <label htmlFor="name">Name</label>
                <input 
                    className="form-control" 
                    id="name" 
                    name="name" 
                    value={this.state.timer.name}
                    onChange={this.handleEvent}
                    autoFocus
                    required
                />
            </div>

            <div className="form-row">
                <div className="form-group col-md-4">
                    <label htmlFor="interval">Interval</label>
                    <div className="input-group">
                        <input 
                            id="interval" 
                            type="number" 
                            className="form-control text-right" 
                            name="interval" 
                            value={this.state.timer.interval}
                            onChange={this.handleEvent}
                            required
                        />
                        <div className="input-group-append">
                            <div className="input-group-text">minutes</div>
                        </div>
                    </div>
                </div>
                <div className="form-group col-md-4">
                    <label htmlFor="enabled_status">Enabled when stream is</label>
                    <select 
                        type="text" 
                        className="form-control" 
                        id="enabled_status" 
                        name="enabled_status" 
                        value={this.state.timer.enabled_status}
                        onChange={this.handleEvent}
                    >
                        <option value="0">{enabledWhenName(0)}</option>
                        <option value="1">{enabledWhenName(1)}</option>
                        <option value="2">{enabledWhenName(2)}</option>
                    </select>
                </div>                
                <div className="form-group col-md-4">
                    <label htmlFor="send_message_order">Message choose order</label>
                    <select 
                        type="text" 
                        className="form-control" 
                        id="send_message_order" 
                        name="send_message_order" 
                        value={this.state.timer.send_message_order}
                        onChange={this.handleEvent}
                    >
                        <option value="1">In order</option>
                        <option value="2">Random order</option>
                    </select>
                </div>
            </div>

            <div className="form-group">
                <div className="custom-control custom-checkbox">
                    <input 
                        name="enabled"
                        type="checkbox" 
                        className="custom-control-input" 
                        id="enabled"
                        checked={this.state.timer.enabled}
                        onChange={this.handleEvent} 
                    />
                    <label className="custom-control-label" htmlFor="enabled">Enabled</label>
                </div>
            </div>

            <div className="form-group">
                <label htmlFor="messages" className="mb-0">Messages (<a href="https://docs.botashell.com" target="_blank">Variables documentation</a>)</label>
                <small className="form-text mb-2 mt-0">
                    One message per line. 1 line will be chosen when the timer triggers.
                </small>
                <textarea 
                    className="form-control" 
                    id="messages" 
                    name="messages" 
                    value={this.state.timer.messages}
                    onChange={this.handleEvent}
                    required
                    rows="5"
                />
            </div>

            {renderError(this.state.error)}
            {this.renderButton()}
            {this.renderDeleteButton()}
        </form>
    }
}

export default Timer
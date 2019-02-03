import React from 'react'
import {Redirect} from 'react-router'
import api from 'tbot/twitch/api'
import Loading from 'tbot/components/loading'
import {setHeader, renderError} from 'tbot/utils'
import {userLevelName, enabledWhenName} from 'tbot/twitch/utils'

class Command extends React.Component {

    constructor(props) {
        super(props)
        this.state = {
            cmd: {
                cmd: '',
                response: '',
                user_level: 0,
                enabled_status: 0,
                global_cooldown: 5,
                user_cooldown: 15,
                mod_cooldown: 0,
                enabled: 1,
                public: 1,
            },
            templates: [],
            loading: true,
            error: null,
            saving: false,
            success: false,
        }
    }

    componentDidMount() {
        if (this.props.match.params.id) {
            setHeader('Edit command')
            this.getCommand()
        } else {            
            setHeader('New command')
            this.getTemplates()
            this.setState({loading: false})
        }
    }

    getCommand() {        
        let id = this.props.match.params.id
        api.get(`/api/twitch/channels/${managedUser.id}/commands/${id}`).then(r => {
            for (let key in r.data) {
                if (!(key in this.state.cmd))
                    delete r.data[key]
            }
            this.setState({
                cmd: r.data, 
                loading: false
            })
            setHeader(`Edit command: !${r.data.cmd}`)
        })
    }

    getTemplates() {        
        let id = this.props.match.params.id
        api.get(`/api/twitch/template-commands`).then(r => {
            this.setState({
                templates: r.data,
            })
        })
    }

    handleEvent = (e) => {
        let val = e.target.type === 'checkbox' ? e.target.checked : e.target.value
        this.state.cmd[e.target.name] = val
        this.setState({cmd: this.state.cmd})
    }

    handleSubmit = (e) => {
        e.preventDefault()
        this.setState({saving: true, error: null})
        let id = this.props.match.params.id
        if (id)
            api.put(`/api/twitch/channels/${managedUser.id}/commands/${id}`, this.state.cmd).then(r => {
                this.setState({success: true})
            }).catch(e => {
                this.setState({error: e.response.data, saving: false})
            })
        else 
            api.post(`/api/twitch/channels/${managedUser.id}/commands`, this.state.cmd).then(r => {
                this.setState({success: true})
            }).catch(e => {
                this.setState({error: e.response.data, saving: false})
            })
    }

    handleDelete = () => {
        if (!confirm(`Delete command: ${this.state.cmd.cmd}?`))
            return
        this.setState({deleting: true, error: null})
        let id = this.props.match.params.id
        api.delete(`/api/twitch/channels/${managedUser.id}/commands/${id}`).then(r => {
            this.setState({
                cmd: r.data, 
                success: true,
            })
        }).catch(e => {
            this.setState({error: e.response.data, deleting: false})
        })
    }

    handleTemplate = (e) => {
        for (let t of this.state.templates) {
            if (t.cmd == e.target.value){
                let d = JSON.parse(JSON.stringify(t))
                for (let key in d) {
                    if (!(key in this.state.cmd))
                        delete d[key]
                }
                this.setState({cmd: d})
            }
        }
    }

    renderButton() {
        if (this.state.saving)
            return <button className="btn btn-primary" type="button" disabled>
                    <span className="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Saving...
                </button>
        return <button type="submit" className="btn btn-primary">Save command</button>
    }

    renderDeleteButton() {
        if (!this.props.match.params.id)
            return null
        if (this.state.deleting)
            return <button className="ml-2 btn btn-danger" type="button" disabled>
                    <span className="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Deleting...
                </button>
        return <button type="button" onClick={this.handleDelete} className="ml-2 btn btn-danger">Delete command</button>
    }

    renderTemplates() {
        if (this.state.templates.length === 0)
            return null
        return <div className="mb-4">
            <label>Templates</label>
            <select className="form-control" onChange={this.handleTemplate}>
                <option value=""></option>
                {this.state.templates.map(temp =>
                    <option key={temp.cmd} value={temp.cmd}>{temp.title}</option>
                )}
            </select>
        </div>
    }

    render() {
        if (this.state.loading)
            return <Loading />
        if (this.state.success)
            return <Redirect to={`/twitch/${this.props.match.params.channel}/commands`} />

        return <div style={{maxWidth:'700px'}}>
            {this.renderTemplates()}
            <form onSubmit={this.handleSubmit}>
            <div className="form-group">
                <label htmlFor="cmd">Command</label>
                <div className="input-group">
                    <div className="input-group-prepend">
                        <div className="input-group-text">!</div>
                    </div>
                    <input 
                        className="form-control" 
                        id="cmd" 
                        name="cmd" 
                        value={this.state.cmd.cmd}
                        onChange={this.handleEvent}
                        autoFocus
                        required
                    />
                </div>
            </div>

            <div className="form-group">
                <label htmlFor="response">Response (<a href="https://docs.botashell.com" target="_blank">Variables documentation</a>)</label>
                <input 
                    className="form-control" 
                    id="response" 
                    name="response" 
                    value={this.state.cmd.response}
                    onChange={this.handleEvent}
                    required
                />
            </div>

            <div className="form-row">
                <div className="form-group col-md-4">
                    <label htmlFor="user_level">User level</label>
                    <select 
                        type="text" 
                        className="form-control" 
                        id="user_level" 
                        name="user_level" 
                        value={this.state.cmd.user_level}
                        onChange={this.handleEvent}
                    >
                        <option value="0">{userLevelName(0)}</option>
                        <option value="1">{userLevelName(1)}</option>
                        <option value="2">{userLevelName(2)}</option>
                        <option value="7">{userLevelName(7)}</option>
                        <option value="8">{userLevelName(8)}</option>
                        <option value="9">{userLevelName(9)}</option>
                    </select>
                </div>
                <div className="form-group col-md-4">
                    <label htmlFor="enabled_status">Enabled when stream is</label>
                    <select 
                        type="text" 
                        className="form-control" 
                        id="enabled_status" 
                        name="enabled_status" 
                        value={this.state.cmd.enabled_status}
                        onChange={this.handleEvent}
                    >
                        <option value="0">{enabledWhenName(0)}</option>
                        <option value="1">{enabledWhenName(1)}</option>
                        <option value="2">{enabledWhenName(2)}</option>
                    </select>
                </div>
            </div>

            <div className="form-row">
                <div className="form-group col-md-4">
                    <label htmlFor="global_cooldown">Global cooldown</label>
                    <input 
                        id="global_cooldown" 
                        type="number" 
                        className="form-control" 
                        name="global_cooldown" 
                        value={this.state.cmd.global_cooldown}
                        onChange={this.handleEvent}
                    />
                </div>
                <div className="form-group col-md-4">
                    <label htmlFor="user_cooldown">User cooldown</label>
                    <input 
                        id="user_cooldown" 
                        type="number" 
                        className="form-control" 
                        name="user_cooldown" 
                        value={this.state.cmd.user_cooldown}
                        onChange={this.handleEvent}
                    />
                </div>
                <div className="form-group col-md-4">
                    <label htmlFor="mod_cooldown">Mod cooldown</label>
                    <input 
                        id="mod_cooldown" 
                        type="number" 
                        className="form-control" 
                        name="mod_cooldown" 
                        value={this.state.cmd.mod_cooldown}
                        onChange={this.handleEvent}
                    />
                </div>
            </div>
            <div className="form-group">
                <div className="custom-control custom-checkbox">
                    <input 
                        name="enabled"
                        type="checkbox" 
                        className="custom-control-input" 
                        id="enabled"
                        checked={this.state.cmd.enabled}
                        onChange={this.handleEvent} 
                    />
                    <label className="custom-control-label" htmlFor="enabled">Enabled</label>
                </div>
            </div>
            <div className="form-group">
                <div className="custom-control custom-checkbox">
                    <input 
                        name="public"
                        type="checkbox" 
                        className="custom-control-input" 
                        id="public"
                        checked={this.state.cmd.public}
                        onChange={this.handleEvent} 
                    />
                    <label className="custom-control-label" htmlFor="public">Public (show it on the command list page)</label>
                </div>
            </div>
            {renderError(this.state.error)}
            {this.renderButton()}
            {this.renderDeleteButton()}
        </form>
        </div>
    }
}

export default Command
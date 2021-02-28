import React from 'react'
import api from 'tbot/twitch/api'
import SaveButton from 'tbot/components/save_button'
import {renderError} from 'tbot/utils'

class DiscordConnect extends React.Component {

    constructor(props) {
        super(props)
        this.state = {
            loading: true,
            saving: false,
            saved: false,
            error: null,
            data: {
                'webhook_url': '',
                'message': '@everyone {name} is LIVE {url}',
            }
        }
    }

    componentDidMount() {
        this.getStatus()
    }

    getStatus() {
        this.setState({loading: true})
        api.get(`/api/twitch/channels/${managedUser.id}/discord-live-notification`).then(r => {
            if (r.data) {
                this.setState({data: r.data, loading: false})
            } else {
                this.setState({loading: false})
            }
        })
    }

    handleSubmit = (e) => {
        e.preventDefault()
        this.setState({saving: true, error: null})
        api.put(`/api/twitch/channels/${managedUser.id}/discord-live-notification`, this.state.data).then(r => {
            this.setState({saved: true, saving: false})
        }).catch(e => {
            this.setState({error: e.response.data, saving: false})
        })
    }

    handleEvent = (e) => {
        this.state.data[e.target.name] = e.target.value
        this.setState({data: this.state.data, saved: false})
    }

    render() {
        return <form style={{maxWidth:'700px'}} onSubmit={this.handleSubmit}>  
            <div className="form-group mb-2">
                <label htmlFor="webhook_url">Webhook URL</label>
                <input 
                    className="form-control" 
                    id="webhook_url" 
                    name="webhook_url" 
                    value={this.state.data.webhook_url}
                    onChange={this.handleEvent}
                />
                <div className="alert alert-info mt-1">In Discord right click on the channel > Edit channel > Webhooks > 
                    Create webhook > Copy the Webhook URL</div>
            </div>            
            <div className="form-group mb-2">
                <label htmlFor="message">Message</label>
                <input 
                    className="form-control" 
                    id="message" 
                    name="message" 
                    value={this.state.data.message}
                    onChange={this.handleEvent}
                />
                <div>Variables: {`{name}`} {`{url}`}</div>
            </div>  
            {renderError(this.state.error)}
            <SaveButton 
                isSaving={this.state.saving} 
                isSaved={this.state.saved}
                savedText={`Saved`}
            >
                Save
            </SaveButton>
        </form>
    }
}

export default DiscordConnect
import React from 'react'
import api from 'tbot/twitch/api'

class DiscordConnect extends React.Component {

    constructor(props) {
        super(props)
        this.state = {
            loading: true,
            discord: {},
            connecting: false,
            deleting: false,
        }
    }

    componentDidMount() {
        this.getStatus()
    }

    getStatus() {
        this.setState({loading: true})
        api.get(`/api/twitch/channels/${managedUser.id}/discord`).then(r => {
            this.setState({discord: r.data, loading: false})
        })
    }

    handleSubmit = () => {
        this.setState({connecting: true})
    }

    handleDelete = (e) => {
        e.preventDefault()
        this.setState({deleting: true})        
        api.delete(`/api/twitch/channels/${managedUser.id}/discord`).then(r => {
            this.setState({discord: {}, deleting: false})
        })
    }

    renderButton() {
        if (this.state.loading) 
            return <button className="btn btn-info" type="button" disabled>
                <span 
                    className="spinner-border spinner-border-sm" 
                    role="status" 
                    aria-hidden="true">
                </span> Loading discord status...
            </button>
        if (this.state.connecting) 
            return <button className="btn btn-info" type="button" disabled>
                <span 
                    className="spinner-border spinner-border-sm" 
                    role="status" 
                    aria-hidden="true">
                </span> Connecting discord...
            </button>
        if (this.state.deleting) 
            return <button className="btn btn-info" type="button" disabled>
                <span 
                    className="spinner-border spinner-border-sm" 
                    role="status" 
                    aria-hidden="true">
                </span> Deleting connection discord...
            </button>
        if (this.state.discord.connected)
            return <button type="submit" className="btn btn-danger">
                Disconnect from Discord
            </button>
        return <button type="submit" className="btn btn-success">
            Connect Discord
        </button>
    }

    render() {
        if (this.state.discord.connected)
            return <div>
                <div className="mb-3">
                    Connected to Discord server: {this.state.discord.name}
                </div>
                <form method="post" onSubmit={this.handleDelete}>
                    {this.renderButton()}
                </form>
            </div>
        return <div>
            <form method="post" onSubmit={this.handleSubmit} action={`/api/twitch/channels/${managedUser.id}/discord`}>
                {this.renderButton()}
            </form>
        </div>
    }
}

export default DiscordConnect
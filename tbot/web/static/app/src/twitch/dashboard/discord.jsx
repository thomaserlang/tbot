import React from 'react'
import api from 'tbot/twitch/api'
import BotControls from './components/bot_controls'
import {setHeader} from 'tbot/utils'
import Loading from 'tbot/components/loading'

class Discord extends React.Component {

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
        setHeader('Discord')
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

    render() {
        if (this.state.loading) 
            return <Loading />
        if (this.state.discord.connected)
            return <div>
                <div className="mb-3">
                    Connected to Discord server: {this.state.discord.name}
                </div>
                <form method="post" onSubmit={this.handleDelete}>
                    <button type="submit" className="btn btn-danger">
                        Disconnect from Discord
                    </button>
                </form>
            </div>
        return <div>
            <form method="post" onSubmit={this.handleSubmit} action={`/api/twitch/channels/${managedUser.id}/discord`}>
                <button type="submit" className="btn btn-success">
                    Connect Discord
                </button>
            </form>
        </div>
    }
}

export default Discord
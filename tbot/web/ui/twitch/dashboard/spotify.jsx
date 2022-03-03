import React from 'react'
import api from 'tbot/twitch/api'
import BotControls from './components/bot_controls'
import {setHeader} from 'tbot/utils'
import Loading from 'tbot/components/loading'

class Spotify extends React.Component {

    constructor(props) {
        super(props)
        this.state = {
            loading: true,
            spotify: {},
            connecting: false,
            deleting: false,
        }
    }

    componentDidMount() {
        setHeader('Spotify')
        this.getStatus()
    }

    getStatus() {
        this.setState({loading: true})
        api.get(`/api/twitch/channels/${managedUser.id}/spotify`).then(r => {
            this.setState({spotify: r.data, loading: false})
        })
    }

    handleSubmit = () => {
        this.setState({connecting: true})
    }

    handleDelete = (e) => {
        e.preventDefault()
        this.setState({deleting: true})        
        api.delete(`/api/twitch/channels/${managedUser.id}/spotify`).then(r => {
            this.setState({spotify: {}, deleting: false})
        })
    }

    render() {
        if (this.state.loading) 
            return <Loading />
        if (this.state.spotify.connected)
            return <div>
                <div className="mb-3">
                    Connected to Spotify account: {this.state.spotify.user}
                </div>
                <form method="post" onSubmit={this.handleDelete}>
                    <button type="submit" className="btn btn-danger">
                        Disconnect Spotify
                    </button>
                </form>
            </div>
        return <div>
            <form method="post" onSubmit={this.handleSubmit} action={`/api/twitch/channels/${managedUser.id}/spotify`}>
                <button type="submit" className="btn btn-success">
                    Connect Spotify
                </button>
            </form>
        </div>
    }
}

export default Spotify
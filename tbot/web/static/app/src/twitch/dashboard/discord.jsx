import React from 'react'
import api from 'tbot/twitch/api'
import {setHeader} from 'tbot/utils'
import Loading from 'tbot/components/loading'
import ConnectButton from './components/discord_connect'
import DiscordLive from './components/discord_live_notification'

class Discord extends React.Component {

    constructor(props) {
        super(props)
        this.state = {
            loading: true,
        }
    }

    componentDidMount() {
        setHeader('Discord')
    }

    render() {
        return <>
            <div className="mb-4">
                <h2>Sub role sync</h2>
                <ConnectButton />
            </div>
            <div>                
                <h2>Live Notification</h2>
                <DiscordLive />
            </div>
        </>
    }
}

export default Discord
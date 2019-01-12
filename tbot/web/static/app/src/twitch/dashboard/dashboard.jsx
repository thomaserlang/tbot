import React from 'react'
import {Redirect} from 'react-router'
import api from 'tbot/twitch/api'
import BotControls from './components/bot_controls'
import {setHeader} from 'tbot/utils'

class Dashboard extends React.Component {

    componentDidMount() {
        setHeader('Dashboard')
    }

    render() {
        if (managedUser.level < 3) 
            return <Redirect to={`/twitch/${managedUser.name}/commands`} />
        return <div className="d-flex">
            <div style={{width: '200px'}}>
                <BotControls />
            </div>
        </div>
    }
}

export default Dashboard
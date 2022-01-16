import React from 'react'
import {Redirect} from 'react-router'
import BotControls from './components/bot_controls'
import Commercial from './components/commercial'
import ExtraAuth from './components/extra_auth'
import {setHeader} from 'tbot/utils'

class Dashboard extends React.Component {

    componentDidMount() {
        setHeader('Dashboard')
    }

    render() {
        if (managedUser.level < 3) 
            return <Redirect to={`/twitch/${managedUser.name}/commands`} />
        return <div className="d-flex">
            <ExtraAuth />
            <div style={{width: '200px'}}>
                <BotControls />
                <Commercial />
            </div>
        </div>
    }
}

export default Dashboard
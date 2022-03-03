import React from 'react'
import {Link} from 'react-router-dom'
import api from 'tbot/twitch/api'
import {isAuthed, requireAuth} from 'tbot/twitch/utils'
import {setTitle} from 'tbot/utils'

import SuggestChannelInput from './suggestchannelinput'

class SelectChannel extends React.Component {

    constructor(props) {
        super(props)
        this.state = {
            modOf: [],
        }
        setTitle('Twitch Logviewer')
        this.twitchLoginClick = this.twitchLoginClick.bind(this);
    }

    twitchLoginClick() {
        requireAuth();
    }

    componentDidMount() {
        api.get('/api/twitch/user/mod-of').then(r => {
            this.setState({
                modOf: r.data,
            })
        })
    }

    renderModOf() {
        if (!isAuthed())
            return null;
        return (
            <div className="mod-of">
                {this.state.modOf.map(c => (
                    <div key={c.id}>
                        <Link to={`/twitch/logviewer/${c.name}`}>
                            {c.name}
                        </Link>
                    </div>
                ))}
            </div>
        )
    }

    renderLoginButton() {
        if (isAuthed())
            return null;
        return (
            <center>
                <button className="btn btn-primary" onClick={this.twitchLoginClick}>Login with Twitch</button>
            </center>
        )
    }

    render() {
        return <div id="select-channels">
            <div className="text-center">
                <Link to="/">{tbot.name}</Link>
            </div>
            <h1>Twitch Logviewer</h1>
            <div className="suggest-channel">
                <SuggestChannelInput />
            </div>
            {this.renderModOf()}
            {this.renderLoginButton()}            
        </div>
    }
}

export default SelectChannel;
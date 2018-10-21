import React from 'react'
import api from 'tbot/api'

import SuggestChannelInput from './suggestchannelinput'

class SelectChannel extends React.Component {

    constructor(props) {
        super(props)
        this.state = {
            modOf: [],
        }
    }

    componentDidMount() {
        document.title = `Twitch Logviewer - ${window.tbot.name}`
        api.get('/api/twitch/user/mod-of').then(r => {
            this.setState({
                modOf: r.data,
            })
        })
    }

    render() {
        return <div id="select-channels">
            <h1>Twitch Logviewer</h1>
            <div className="suggest-channel">
                <SuggestChannelInput />
            </div>
            <div className="mod-of">
                {this.state.modOf.map(c => (
                    <div key={c.id}>
                        <a href={`/twitch/logviewer/${c.name}`}>
                            {c.name}
                        </a>
                    </div>
                ))}
            </div>
        </div>
    }
}

export default SelectChannel;
import React from 'react'
import './front.scss'

class Front extends React.Component {

    render() {
        return <div id="front">
            <div className="title">
                {window.tbot.name}
            </div>
            <div className="items">
                <div className="title">
                    Twitch
                </div>
                <a href="/twitch/bot" className="item twitch">                    
                    Bot Settings
                </a>
                <a href="/twitch/logviewer" className="item twitch">
                    Logviewer
                </a>
            </div>
            <div className="items">
                <div className="title">
                    Discord
                </div>
                <a className="item discord">
                    Bot Settings
                </a>
                <a className="item discord">
                    Logviewer
                </a>
            </div>
        </div>
    }
}

export default Front
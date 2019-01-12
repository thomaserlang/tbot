import React from 'react'
import './front.scss'

class Front extends React.Component {

    render() {
        return <div id="front">
            <div className="items">
                <div className="title">
                    Twitch
                </div>
                <a href="/twitch/dashboard" className="item twitch">                    
                    Dashboard
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
                    Dashboard
                </a>
                <a className="item discord">
                    Logviewer
                </a>
            </div>
        </div>
    }
}

export default Front
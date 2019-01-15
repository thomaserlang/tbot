import React from 'react'
import {Link} from 'react-router-dom'
import './front.scss'

class Front extends React.Component {

    render() {
        return <div id="front">
            <div className="items">
                <div className="title">
                    Twitch
                </div>
                <Link to="/twitch/dashboard" className="item twitch">                    
                    Dashboard
                </Link>
                <Link to="/twitch/logviewer" className="item twitch">
                    Logviewer
                </Link>
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
import React from 'react'
import {NavLink} from 'react-router-dom'

import './topbar.scss'

class Sidebar extends React.Component {

    render() {
        return (
            <div id="topbar" className="sticky-top">
                <div className="title" id="top-title"></div>
                <div className="signed-as">Signed in as <b>{tbot['twitch_user']['user']}</b>, <a href="/twitch/logout">log out</a></div>
            </div>
        )
    }

}

export default Sidebar
import React from 'react'
import {NavLink} from 'react-router-dom'
import SelectChannel from './select_channel.jsx'
import './sidebar.scss'

class Sidebar extends React.Component {

    constructor(props) {
        super(props)
        this.state = {
            showSelectChannel: false,
        }
    }

    onClose = () => {
        this.setState({showSelectChannel: false})
    }

    selectChannelClick = (e) => {
        this.setState({showSelectChannel: true})
    }

    renderConnect() {
        if (managedUser.level < 3)
            return null
        return <span> 
            <div className="title">CONNECT</div>
            <NavLink to={`/twitch/${managedUser.name}/spotify`} activeClassName="active">Spotify</NavLink> 
            <NavLink to={`/twitch/${managedUser.name}/discord`} activeClassName="active">Discord</NavLink> 
            <NavLink to={`/twitch/${managedUser.name}/youtube`} activeClassName="active">YouTube</NavLink> 
        </span>
    }    

    renderPoints() {
        if (managedUser.level < 3)
            return null
        return <span> 
            <div className="title">GAMBLING</div>
            <NavLink to={`/twitch/${managedUser.name}/points-settings`} activeClassName="active">Points Settings</NavLink> 
            <NavLink to={`/twitch/${managedUser.name}/gambling-slots-settings`} activeClassName="active">Slots Settings</NavLink> 
            <NavLink to={`/twitch/${managedUser.name}/gambling-roulette-settings`} activeClassName="active">Roulette Settings</NavLink> 
        </span>
    }


    render() {
        return (
            <div id="sidebar" className="sticky-top">
                <div 
                    className="d-flex" 
                    id="managed-user" 
                    title="Click to change channel"
                    onClick={this.selectChannelClick}
                >                    
                    <div className="menuicon"><i className="material-icons">menu</i></div>
                    <div className="user">
                        {managedUser.name}
                    </div>
                    <div className="menuicon ml-auto"><i className="material-icons">arrow_drop_down</i></div>
                </div>
                <div id="items">
                    {managedUser.level >= 3 ?               
                        <NavLink to={`/twitch/${managedUser.name}/dashboard`} activeClassName="active">Dashboard</NavLink>
                    : null }
                    
                    <NavLink to={`/twitch/${managedUser.name}/commands`} activeClassName="active">Commands</NavLink>
                    <NavLink to={`/twitch/${managedUser.name}/timers`} activeClassName="active">Timers</NavLink>
                    <NavLink to={`/twitch/${managedUser.name}/filters`} activeClassName="active">Filters</NavLink>
                    <NavLink to={`/twitch/${managedUser.name}/banned-words`} activeClassName="active">Banned words</NavLink>
                    <NavLink to={`/twitch/${managedUser.name}/chat-alerts`} activeClassName="active">Chat alerts</NavLink>
                    <NavLink to={`/twitch/${managedUser.name}/quotes`} activeClassName="active">Quotes</NavLink>
                    
                    {managedUser.level >= 3 ?
                        <NavLink to={`/twitch/${managedUser.name}/admins`} activeClassName="active">Admins</NavLink>
                    : null }

                    {this.renderPoints()}

                    {this.renderConnect()}

                    <div className="title">LINKS</div>
                    <NavLink to={`/twitch/logviewer/${managedUser.name}`}>Logviewer</NavLink> 
                    <NavLink to={`/live-chat/${managedUser.id}`}>Live chat</NavLink> 

                </div>
                {this.state.showSelectChannel?
                    <SelectChannel onClose={this.onClose} />
                :null}
            </div>
        )
    }

}

export default Sidebar
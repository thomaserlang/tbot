import React from 'react'
import api from 'tbot/twitch/api'

class BotControls extends React.Component {

	constructor(props) {
		super(props)
        this.state = {
            settings: null,
        }
	}

    componentDidMount() {
        this.getSettings()
    }

    getSettings() {
        api.get(`/api/twitch/channels/${managedUser.id}/bot-settings`).then(r => {
            this.setState({settings: r.data})
        })
    }

	joinClick = () => {
		api.post(`/api/twitch/channels/${managedUser.id}/bot-join`).then(r => {
   			this.getSettings();
        })
	}

    partClick = () => {
        api.delete(`/api/twitch/channels/${managedUser.id}/bot-join`).then(r => {
            this.getSettings();
        })
    }

    muteClick = () => {
        api.post(`/api/twitch/channels/${managedUser.id}/bot-mute`).then(r => {
            this.getSettings();
        })
    }

    unmuteClick = () => {
        api.delete(`/api/twitch/channels/${managedUser.id}/bot-mute`).then(r => {
            this.getSettings();
        })
    }

    enableChatlogClick = () => {
        api.post(`/api/twitch/channels/${managedUser.id}/bot-enable-chatlog`).then(r => {
            this.getSettings();
        })
    }

    disableChatlogClick = () => {
        api.delete(`/api/twitch/channels/${managedUser.id}/bot-enable-chatlog`).then(r => {
            this.getSettings();
        })
    }

    render() {
        if (!this.state.settings)
            return null;
        return <div className="box">
            <div className="title">Bot Controls</div>
            <div className="buttons">
                {!this.state.settings.active?
                    <button className="btn btn-success" onClick={this.joinClick}>Join channel</button>
                :null}
                {this.state.settings.active?
                    <button className="btn btn-danger" onClick={this.partClick}>Part channel</button>
                :null}

                {!this.state.settings.muted?
                    <button className="btn btn-secondary" onClick={this.muteClick}>Mute bot</button>
                :null}
                {this.state.settings.muted?
                    <button className="btn btn-secondary" onClick={this.unmuteClick}>Unmute bot</button>
                :null}         

                {!this.state.settings.chatlog_enabled?
                    <button className="btn btn-secondary" onClick={this.enableChatlogClick}>Enable chatlog</button>
                :null}
                {this.state.settings.chatlog_enabled?
                    <button className="btn btn-secondary" onClick={this.disableChatlogClick}>Disable chatlog</button>
                :null}
            </div>
        </div>
    }
}

export default BotControls
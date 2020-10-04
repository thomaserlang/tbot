import React from 'react'
import {Link} from 'react-router-dom'
import api from 'tbot/twitch/api'
import Loading from 'tbot/components/loading'
import {setHeader, renderError} from 'tbot/utils'
import SaveButton from 'tbot/components/save_button'

class GamblingSlots extends React.Component {

    constructor(props) {
        super(props)
        this.state = {
            loading: true,
            saving: false,
            saved: false,
            settings: {
                emote_pool_size: 4,
                emotes: 'MrDestructoid SeriousSloth OSFrog OhMyDog',
                payout_percent: 95,
                min_bet: 5,
                max_bet: 0,
                win_message: '@{user} {emotes} you won {bet} {points_name} and now have {points} {points_name}',
                allin_win_message: '@{user} {emotes} you WON {bet} {points_name} and now have {points} {points_name} EZ',
                lose_message: '@{user} {emotes} you lost {bet} {points_name}',
                allin_lose_message: '@{user} {emotes} you lost {bet} {points_name} PepeLaugh',
            }
        }
    }

    componentDidMount() {
        setHeader('Gambling - Slots Settings')
        this.getSettings()
    }

    getSettings() {
        api.get(`/api/twitch/channels/${managedUser.id}/gambling-slots-settings`).then(r => {
            if (r.data) {
                r.data.emotes = r.data.emotes.join(' ')
                this.setState({
                    loading: false,
                    settings: r.data,
                })
            } else {
                this.setState({
                    loading: false,
                })
            }
        })
    }
    
    handleEvent = (e) => {
        let val = e.target.type === 'checkbox' ? e.target.checked : e.target.value
        this.state.settings[e.target.name] = val
        this.setState({
            settings: this.state.settings,
            saved: false,
        })
    }

    handleSubmit = (e) => {        
        e.preventDefault()
        this.setState({saving: true})
        if (!Array.isArray(this.state.settings.emotes))
            this.state.settings.emotes = this.state.settings.emotes.split(' ')
        this.state.settings.emotes = this.state.settings.emotes.filter(e => (
            e != ''
        ))
        api.put(`/api/twitch/channels/${managedUser.id}/gambling-slots-settings`, this.state.settings).then(r => {
            this.state.settings.emotes = this.state.settings.emotes.join(' ')
            this.setState({saving: false, saved: true})
        }).catch(e => {
            this.state.settings.emotes = this.state.settings.emotes.join(' ')
            this.setState({saving: false})
        })
    }

    render() {
        if (this.state.loading)
            return <Loading />
        return <form style={{maxWidth:'700px'}} onSubmit={this.handleSubmit}>
            <div className="d-flex mb-2">
                <div className="form-group">
                    <label htmlFor="emote_pool_size">Emote pool size</label>
                    <input 
                        className="form-control" 
                        id="emote_pool_size" 
                        name="emote_pool_size"
                        type="number"
                        value={this.state.settings.emote_pool_size}
                        onChange={this.handleEvent}
                        style={{width: '200px'}}
                    />
                </div>

                <div className="form-group ml-2">
                    <label htmlFor="payout_percent">Payout percent</label>
                    <input 
                        className="form-control" 
                        id="payout_percent" 
                        name="payout_percent"
                        type="number"
                        value={this.state.settings.payout_percent}
                        onChange={this.handleEvent}
                        style={{width: '200px'}}
                    />
                </div>
            </div>

            <div className="d-flex mb-2">
                <div className="form-group">
                    <label htmlFor="min_bet">Min bet</label>
                    <input 
                        className="form-control" 
                        id="min_bet" 
                        name="min_bet"
                        type="number"
                        value={this.state.settings.min_bet}
                        onChange={this.handleEvent}
                        style={{width: '200px'}}
                    />
                </div>

                <div className="form-group ml-2">
                    <label htmlFor="max_bet">Max bet</label>
                    <input 
                        className="form-control" 
                        id="max_bet" 
                        name="max_bet"
                        type="number"
                        value={this.state.settings.max_bet}
                        onChange={this.handleEvent}
                        style={{width: '200px'}}
                    />
                </div>
            </div>

            <div className="form-group">
                <label htmlFor="emotes">Emotes (separate with a space)</label>
                <div className="input-group" style={{maxWidth: '700px'}}>
                    <textarea 
                        className="form-control" 
                        name="emotes" 
                        value={this.state.settings.emotes}
                        onChange={this.handleEvent}
                        rows="2"
                    />
                </div>
            </div>

            <div className="form-group">
                <label htmlFor="win_message">Win message</label>                
                <input 
                    className="form-control" 
                    id="win_message" 
                    name="win_message"
                    type="text"
                    value={this.state.settings.win_message}
                    onChange={this.handleEvent}
                />
            </div>

            <div className="form-group">
                <label htmlFor="allin_win_message">All-in win message</label>                
                <input 
                    className="form-control" 
                    id="allin_win_message" 
                    name="allin_win_message"
                    type="text"
                    value={this.state.settings.allin_win_message}
                    onChange={this.handleEvent}
                />
            </div>

            <div className="form-group">
                <label htmlFor="lose_message">Lose message</label>                
                <input 
                    className="form-control" 
                    id="lose_message" 
                    name="lose_message"
                    type="text"
                    value={this.state.settings.lose_message}
                    onChange={this.handleEvent}
                />
            </div>

            <div className="form-group">
                <label htmlFor="allin_lose_message">All-in lose message</label>                
                <input 
                    className="form-control" 
                    id="allin_lose_message" 
                    name="allin_lose_message"
                    type="text"
                    value={this.state.settings.allin_lose_message}
                    onChange={this.handleEvent}
                />
            </div>

            <div>Vars for win and lose messages: <pre>{'{'}user{'}'} {'{'}emotes{'}'} {'{'}bet{'}'} {'{'}points{'}'} {'{'}points_name{'}'}</pre></div>
                
            
            {renderError(this.state.error)}
            <SaveButton 
                isSaving={this.state.saving} 
                isSaved={this.state.saved}
                savedText="Settings saved"
                text="Save settings"
            >Save settings</SaveButton>
        </form>
    }
}

export default GamblingSlots
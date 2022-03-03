import React from 'react'
import {Link} from 'react-router-dom'
import api from 'tbot/twitch/api'
import Loading from 'tbot/components/loading'
import {setHeader, renderError} from 'tbot/utils'
import SaveButton from 'tbot/components/save_button'

class PointsSettings extends React.Component {

    constructor(props) {
        super(props)
        this.state = {
            loading: true,
            saving: false,
            saved: false,
            settings: {
                enabled: false,
                points_name: 'Points',
                points_per_min: 1,
                points_per_min_sub_multiplier: 1,
                points_per_sub: 500,
                points_per_cheer: 1,
                ignore_users: [],
            }
        }
    }

    componentDidMount() {
        setHeader('Points Settings')
        this.getSettings()
    }

    getSettings() {
        api.get(`/api/twitch/channels/${managedUser.id}/points-settings`).then(r => {
            if (r.data) {
                r.data.ignore_users = r.data.ignore_users.join(' ')
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
        if (!Array.isArray(this.state.settings.ignore_users))
            this.state.settings.ignore_users = this.state.settings.ignore_users.split(' ')
        this.state.settings.ignore_users = this.state.settings.ignore_users.filter(e => (
            e != ''
        ))
        api.put(`/api/twitch/channels/${managedUser.id}/points-settings`, this.state.settings).then(r => {
            this.state.settings.ignore_users = this.state.settings.ignore_users.join(' ')
            this.setState({saving: false, saved: true})
        }).catch(e => {
            this.state.settings.ignore_users = this.state.settings.ignore_users.join(' ')
            this.setState({saving: false})
        })
    }

    render() {
        if (this.state.loading)
            return <Loading />
        return <form style={{maxWidth:'700px'}} onSubmit={this.handleSubmit}>
            <div className="form-group">
                <div className="custom-control custom-checkbox">
                    <input 
                        name="enabled"
                        type="checkbox" 
                        className="custom-control-input" 
                        id="enabled"
                        checked={this.state.settings.enabled}
                        onChange={this.handleEvent} 
                    />
                    <label className="custom-control-label" htmlFor="enabled">Enable points</label>
                </div>
            </div>


            <div className="form-group mb-2">
                <label htmlFor="points_name">Points name</label>
                <input 
                    className="form-control" 
                    id="points_name" 
                    name="points_name"
                    type="text"
                    value={this.state.settings.points_name}
                    onChange={this.handleEvent}
                    style={{width: '200px'}}
                />
            </div>

            <div className="d-flex mb-2">
                <div className="form-group">
                    <label htmlFor="points_per_min">Points per min</label>
                    <input 
                        className="form-control" 
                        id="points_per_min" 
                        name="points_per_min"
                        type="number"
                        value={this.state.settings.points_per_min}
                        onChange={this.handleEvent}
                        style={{width: '200px'}}
                    />
                </div>

                <div className="form-group ml-2">
                    <label htmlFor="points_per_min_sub_multiplier">Sub multiplier</label>
                    <input 
                        className="form-control" 
                        id="points_per_min_sub_multiplier" 
                        name="points_per_min_sub_multiplier"
                        type="number"
                        value={this.state.settings.points_per_min_sub_multiplier}
                        onChange={this.handleEvent}
                        style={{width: '200px'}}
                    />
                </div>
            </div>

            <div className="d-flex mb-2">
                <div className="form-group">
                    <label htmlFor="points_per_sub">Points per sub</label>
                    <input 
                        className="form-control" 
                        id="points_per_sub" 
                        name="points_per_sub"
                        type="number"
                        value={this.state.settings.points_per_sub}
                        onChange={this.handleEvent}
                        style={{width: '200px'}}
                    />
                </div>

                <div className="form-group ml-2">
                    <label htmlFor="points_per_cheer">Points per cheer</label>
                    <input 
                        className="form-control" 
                        id="points_per_cheer" 
                        name="points_per_cheer"
                        type="number"
                        value={this.state.settings.points_per_cheer}
                        onChange={this.handleEvent}
                        style={{width: '200px'}}
                    />
                </div>
            </div>


            <div className="form-group">
                <label htmlFor="ignore_users">Ignore users (separate with a space)</label>
                <div className="input-group" style={{maxWidth: '700px'}}>
                    <textarea 
                        className="form-control" 
                        name="ignore_users" 
                        value={this.state.settings.ignore_users}
                        onChange={this.handleEvent}
                        rows="2"
                    />
                </div>
            </div>
            
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

export default PointsSettings
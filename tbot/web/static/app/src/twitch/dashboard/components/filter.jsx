import React from 'react'
import {userLevelName} from 'tbot/twitch/utils'

class Filter extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            loading: true,
            saving: false,
            saved: false,
            error: null,
            filter: {
                enabled: false,
                exclude_user_level: 1,
                warning_enabled: true,
                warning_message: '',
                warning_expire: 3600,
                timeout_message: '',
                timeout_duration: 60,
            },
        }
    }

    handleEvent = (e) => {
        let val = e.target.type === 'checkbox' ? e.target.checked : e.target.value
        this.state.filter[e.target.name] = val
        this.setState({filter: this.state.filter})
    }

    renderBase() {
        return <>
            <div className="form-group mb-4" style={{width: '200px'}}>
                <label htmlFor="exclude_user_level">Exclude user level</label>
                <select 
                    type="text" 
                    className="form-control" 
                    id="exclude_user_level" 
                    name="exclude_user_level" 
                    value={this.state.filter.exclude_user_level}
                    onChange={this.handleEvent}
                >
                    <option value="1">{userLevelName(1)}</option>
                    <option value="2">{userLevelName(2)}</option>
                    <option value="7">{userLevelName(7)}</option>
                </select>
            </div>

            <h5>Warning</h5>
            <div className="form-group mb-2">
                <div className="custom-control custom-checkbox">
                    <input 
                        name="warning_enabled"
                        type="checkbox" 
                        className="custom-control-input" 
                        id="warning_enabled"
                        checked={this.state.filter.warning_enabled}
                        onChange={this.handleEvent} 
                    />
                    <label className="custom-control-label" htmlFor="warning_enabled">Enable warning</label>
                </div>
            </div>
            <div className="form-group mb-2">
                <label htmlFor="warning_message">Warning message</label>
                <input 
                    className="form-control" 
                    id="warning_message" 
                    name="warning_message" 
                    value={this.state.filter.warning_message}
                    onChange={this.handleEvent}
                />
            </div>
            <div className="form-group mb-4">
                <label htmlFor="warning_expire">Warning expires after</label>
                <div className="input-group" style={{width: '160px'}}>
                    <input 
                        id="warning_expire" 
                        type="number" 
                        className="form-control text-right" 
                        name="warning_expire" 
                        value={this.state.filter.warning_expire}
                        onChange={this.handleEvent}
                        required
                    />
                    <div className="input-group-append">
                        <div className="input-group-text">seconds</div>
                    </div>
                </div>
            </div>

            <h5>Timeout</h5>
            <div className="form-group mb-2">
                <label htmlFor="timeout_message">Timeout message</label>
                <input 
                    className="form-control" 
                    id="timeout_message" 
                    name="timeout_message" 
                    value={this.state.filter.timeout_message}
                    onChange={this.handleEvent}
                />
            </div>
            <div className="form-group">
                <label htmlFor="timeout_duration">Timeout duration</label>
                <div className="input-group" style={{width: '160px'}}>
                    <input 
                        id="timeout_duration" 
                        type="number" 
                        className="form-control text-right" 
                        name="timeout_duration" 
                        value={this.state.filter.timeout_duration}
                        onChange={this.handleEvent}
                        required
                    />
                    <div className="input-group-append">
                        <div className="input-group-text">seconds</div>
                    </div>
                </div>
            </div>
        </>
    }
}

export default Filter
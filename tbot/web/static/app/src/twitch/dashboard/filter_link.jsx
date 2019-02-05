import React from 'react'
import {Redirect} from 'react-router'
import api from 'tbot/twitch/api'
import {setHeader, renderError} from 'tbot/utils'
import Loading from 'tbot/components/loading'
import SaveButton from 'tbot/components/save_button'
import Filter from './components/filter'

class Filter_link extends Filter {

    constructor(props) {
        super(props)
        this.state.filter.warning_message = '@{sender}, You are not permitted to post links [warning]'
        this.state.filter.timeout_message = '@{sender}, You are not permitted to post links'
        this.state.filter.whitelist = []
    }

    componentDidMount() {
        setHeader('Link filter')
        this.getFilters()
    }

    getFilters() {
        api.get(`/api/twitch/channels/${managedUser.id}/filters/link`).then(r => {
            if (!r.data) {
                this.setState({loading: false})
                return
            }
            for (let key in r.data) {
                if (!(key in this.state.filter))
                    delete r.data[key]
            }
            r.data.whitelist = r.data.whitelist.join('\n')
            this.setState({
                loading: false,
                filter: r.data,
            })
        })
    }

    submit = (e) => {
        e.preventDefault()
        if (!Array.isArray(this.state.filter.whitelist))
            this.state.filter.whitelist = this.state.filter.whitelist.split('\n')
        this.state.filter.whitelist = this.state.filter.whitelist.filter(e => (
            e != ''
        ))
        api.put(`/api/twitch/channels/${managedUser.id}/filters/link`, this.state.filter).then(r => {
            this.setState({saved: true})
        }).catch(e => {            
            this.state.filter.whitelist = this.state.filter.whitelist.join('\n')
            this.setState({error: e.response.data, saving: false})
        })
    }

    render() {
        if (this.state.loading)
            return <Loading text="Loading filter" />
        if (this.state.saved)
            return <Redirect to={`/twitch/${managedUser.name}/filters`} />
        return <form style={{maxWidth:'700px'}} onSubmit={this.submit}>
            <div className="form-group">
                <div className="custom-control custom-checkbox">
                    <input 
                        name="enabled"
                        type="checkbox" 
                        className="custom-control-input" 
                        id="enabled"
                        checked={this.state.filter.enabled}
                        onChange={this.handleEvent} 
                    />
                    <label className="custom-control-label" htmlFor="enabled">Enable Link filter</label>
                </div>
            </div>

            <div className="form-group">
                <label htmlFor="timeout_duration">Whitelist (1 domain per line, e.g. youtube.com)</label>
                <div className="input-group" style={{width: '200px'}}>
                    <textarea 
                        className="form-control" 
                        name="whitelist" 
                        value={this.state.filter.whitelist}
                        onChange={this.handleEvent}
                        rows="2"
                    />
                </div>
            </div>

            {this.renderBase()}
            
            {renderError(this.state.error)}
            <SaveButton isSaving={this.state.saving} text="Save filter">Save filter</SaveButton>
        </form>
    }

}

export default Filter_link
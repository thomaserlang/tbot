import React from 'react'
import {Redirect} from 'react-router'
import api from 'tbot/twitch/api'
import {setHeader, renderError} from 'tbot/utils'
import Loading from 'tbot/components/loading'
import SaveButton from 'tbot/components/save_button'
import Filter from './components/filter'

class Filter_symbol extends Filter {

    constructor(props) {
        super(props)
        this.state.filter.warning_message = 'Your message was too long [warning]'
        this.state.filter.timeout_message = 'Your message was too long'
        this.state.filter.max_length = 350
    }

    componentDidMount() {
        setHeader('Paragraph filter')
        this.getFilters()
    }

    getFilters() {
        api.get(`/api/twitch/channels/${managedUser.id}/filters/paragraph`).then(r => {
            if (!r.data) {
                this.setState({loading: false})
                return
            }
            for (let key in r.data) {
                if (!(key in this.state.filter))
                    delete r.data[key]
            }
            this.setState({
                loading: false,
                filter: r.data,
            })
        })
    }

    submit = (e) => {
        e.preventDefault()
        api.put(`/api/twitch/channels/${managedUser.id}/filters/paragraph`, this.state.filter).then(r => {
            this.setState({saved: true})
        }).catch(e => {
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
                    <label className="custom-control-label" htmlFor="enabled">Enable Paragraph filter</label>
                </div>
            </div>

            <div className="form-group mb-2">
                <label htmlFor="max_length">Max length</label>
                <input 
                    className="form-control" 
                    id="max_length" 
                    name="max_length"
                    type="number"
                    value={this.state.filter.max_length}
                    onChange={this.handleEvent}
                    style={{width: '200px'}}
                />
            </div>

            {this.renderBase()}
            
            {renderError(this.state.error)}
            <SaveButton isSaving={this.state.saving} text="Save filter">Save filter</SaveButton>
        </form>
    }

}

export default Filter_symbol
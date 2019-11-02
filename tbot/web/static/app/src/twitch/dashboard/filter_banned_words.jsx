import React from 'react'
import {Redirect} from 'react-router'
import api from 'tbot/twitch/api'
import {setHeader, renderError} from 'tbot/utils'
import Loading from 'tbot/components/loading'
import SaveButton from 'tbot/components/save_button'
import Filter from './components/filter'

class Filter_banned_words extends Filter {

    constructor(props) {
        super(props)
        this.state.filter.name = ''
        this.state.filter.enabled = true
        this.state.filter.warning_message = '@{sender}, Banned word [warning]'
        this.state.filter.timeout_message = '@{sender}, Banned word'
        this.state.filter.timeout_duration = 86400,
        this.state.filter.warning_enabled = false
        this.state.filter.banned_words = [{
            id: null,
            banned_words: '',
        }]
        this.state.changed_banned_words = []
        this.state.saved = false
        this.state.errors = {}
        this.state.testing = false
        this.state.testResult = null
        this.state.redirect_back = false
        this.filter_id = this.props.match.params.id
    }

    componentDidMount() {
        if (this.filter_id) {
            setHeader('Edit banned words group')
            this.getFilter()
        } else {            
            setHeader('New banned words group')
            this.setState({loading: false})
        }
    }

    getFilter() {
        let id = this.filter_id
        api.get(`/api/twitch/channels/${managedUser.id}/filters/banned-words-groups/${id}`).then(r => {
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

    handleSubmit = (e) => {
        e.preventDefault()
        this.setState({'saving': true})
        let data = {...this.state.filter}
        delete data.banned_words
        let id = this.filter_id
        if (id) {
            api.put(`/api/twitch/channels/${managedUser.id}/filters/banned-words-groups/${id}`, data).then(r => {
                this.setState({saving: false, saved: true})
            }).catch(e => {
                this.setState({error: e.response.data, saving: false})
            })
        } else {
            api.post(`/api/twitch/channels/${managedUser.id}/filters/banned-words-groups`, data).then(r => {
                console.log(r.data)
                this.filter_id = r.data.id
                this.setState({saving: false, saved: true})
            }).catch(e => {
                this.setState({error: e.response.data, saving: false})
            })            
        }
    }

    handleBannedWordsChange = (e) => {
        this.state.testResult = null
        let d = this.state.filter.banned_words[e.target.dataset.id]
        d.banned_words = e.target.value
        if (!this.state.changed_banned_words.includes(d))
            this.state.changed_banned_words.push(d)
        this.setState(this.state)
    }

    handleSaveBannedWords = (e) => {
        this.setState({testResult: null})
        let idx = e.target.dataset.id
        let d = this.state.filter.banned_words[idx]
        let filter_id = this.filter_id
        if (d.id) {
            api.put(`/api/twitch/channels/${managedUser.id}/filters/banned-words-groups/${filter_id}/banned-words/${d.id}`, {
                'banned_words': d.banned_words,
            }).then(r => {
                this.setState({
                    changed_banned_words: this.state.changed_banned_words.filter(item => item != d),
                    errors: {},
                })
            }).catch(e => {
                this.setState({errors: {
                    [idx]: e.response.data,
                }})
            })
        } else {
            api.post(`/api/twitch/channels/${managedUser.id}/filters/banned-words-groups/${filter_id}/banned-words`, {
                'banned_words': d.banned_words,
            }).then(r => {
                d.id = r.data.id
                this.setState({
                    changed_banned_words: this.state.changed_banned_words.filter(item => item != d),
                    errors: {},
                })
            }).catch(e => {
                this.setState({errors: {
                    [idx]: e.response.data,
                }})
            })
        }
    }

    handleDeleteBannedWords = (e) => {
        this.setState({testResult: null})
        let idx = e.target.dataset.id
        let d = this.state.filter.banned_words[idx]
        let filter_id = this.filter_id      
        if (!d.id) {
            this.removeBannedWords(d)
            return
        }
        api.delete(`/api/twitch/channels/${managedUser.id}/filters/banned-words-groups/${filter_id}/banned-words/${d.id}`).then(r => {
            this.removeBannedWords(d)
        }).catch(e => {
            this.setState({errors: {
                [idx]: e.response.data,
            }})
        })  
    }

    removeBannedWords(d) {
        let f = {...this.state.filter}
        f.banned_words = f.banned_words.filter(item => item != d)
        this.setState({
            changed_banned_words: this.state.changed_banned_words.filter(item => item != d),
            filter: f,
            errors: {},
        })
    }

    handleAdd = (e) => {
        this.setState({testResult: null})
        this.state.filter.banned_words.push({
            id: null,
            banned_words: '',
        })
        this.setState(this.state)
    }

    handleTest = (e) => {
        e.preventDefault()
        this.setState({
            testing: true,
            testResult: null,
        })
        api.post(`/api/twitch/channels/${managedUser.id}/filters/banned-words-groups/${this.filter_id}/test`, {
            'message': e.target.elements.message.value,
        }).then(r => {
            this.setState({
                testing: false,
                testResult: r.data.match,
            })
        }).catch(e => {
            this.setState({
                error: e.response.data,
                testing: false,
                testResult: null,
            })
        })  
    }

    handleTestChange = (e) => {
        this.setState({
            testResult: null,
        })
    }

    renderTest() {
        return <form 
                className="d-flex"
                onSubmit={this.handleTest}
            >
            <div 
                className="flex-grow-1"
                style={{'width': '240px'}}
            >
                <input 
                    className="form-control"
                    placeholder="Test a message for a match"
                    name="message"
                    onChange={this.handleTestChange}
                />
            </div>
            <div className="ml-2">
                <SaveButton
                    savingTest={'Testing'}
                    savedText={'Matched'}
                    errorText={'Didn\'t match'}
                    isSaving={this.state.testing}
                    isSaved={this.state.testResult}
                    hasError={this.state.testResult === false}

                >
                    Test
                </SaveButton>
            </div>
        </form>
    }

    renderBannedWords() {
        return <>
            {this.state.filter.banned_words.map((bw, idx) => (
                <div key={`bw-${idx}`}>
                <div className='d-flex mb-2'>
                    <div className='flex-grow-1'>
                        <input 
                            className="form-control"
                            value={bw.banned_words}
                            data-id={idx}
                            onChange={this.handleBannedWordsChange}
                        />
                    </div>
                    {this.state.changed_banned_words.includes(bw)?
                        <div>
                            <button 
                                title="Save"
                                type="button" 
                                className="btn btn-secondary ml-2"
                                data-id={idx}
                                onClick={this.handleSaveBannedWords}
                            >Save</button>
                        </div>:''
                    }
                    <div>
                        <button 
                            title="Delete"
                            type="button" 
                            className="btn btn-secondary ml-2"
                            data-id={idx}
                            onClick={this.handleDeleteBannedWords}
                        >×</button>
                    </div>
                </div>
                {this.state.errors[idx]?renderError(this.state.errors[idx]):''}
                </div>
            ))}
            <div className="d-flex">
                <div className="flex-shring-1">
                    <button 
                        type="button" 
                        className="btn btn-secondary"
                        onClick={this.handleAdd}
                    >
                        Add
                    </button>
                </div>
                <div className="ml-auto">
                    {this.renderTest()}
                </div>
            </div>
        </>
    }

    handleDelete = (e) => {
        if (!confirm(`Delete this filter?`))
            return
        api.delete(`/api/twitch/channels/${managedUser.id}/filters/banned-words-groups/${this.filter_id}`).then(r => {
            this.setState({
                redirect_back: true,
            })
        })
    }

    render() {
        if (this.state.loading)
            return <Loading text="Loading filter" />
        if (this.state.saved && !this.props.match.params.id)
            return <Redirect to={`/twitch/${managedUser.name}/banned-words/edit/${this.filter_id}`} />
        if (this.state.redirect_back)
            return <Redirect to={`/twitch/${managedUser.name}/banned-words`} />
        return <div style={{maxWidth:'700px'}}>
            {this.filter_id?
                <div className="mb-4">
                    <h5>Banned words</h5>
                    <p className="mb-1">Use the prefix: "re:" for a regular expression.</p>
                    {this.renderBannedWords()}
                </div>
            : ''}
            <form onSubmit={this.handleSubmit}>
            <div className="form-group">
                <label htmlFor="name">Group name</label>
                <input 
                    className="form-control" 
                    id="name" 
                    name="name" 
                    value={this.state.filter.name}
                    onChange={this.handleEvent}
                    autoFocus={true}
                    required={true}
                />
            </div>
            {this.filter_id?
                <>
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
                        <label className="custom-control-label" htmlFor="enabled">Enabled</label>
                    </div>
                </div>
                {this.renderBase()}
                </>
            : ''
            }

            {renderError(this.state.error)}

            <div className="mt-2">
                <SaveButton 
                    isSaving={this.state.saving} 
                    text="Save"
                >
                    {this.props.match.params.id?'Save':'Create group'}
                </SaveButton>
                {this.filter_id?
                    <button
                        type="button"
                        className="btn btn-danger ml-2"
                        onClick={this.handleDelete}
                    >
                        Delete
                    </button>: ''}
            </div>
        </form>
        </div>
    }

}

export default Filter_banned_words
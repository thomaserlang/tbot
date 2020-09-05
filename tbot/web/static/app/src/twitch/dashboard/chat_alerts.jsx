import React from 'react'
import api from 'tbot/twitch/api'
import {setHeader, renderError} from 'tbot/utils'
import Loading from 'tbot/components/loading'
import SaveButton from 'tbot/components/save_button'

class ChatAlerts extends React.Component {

    constructor(props) {
        super(props)
        this.state = {
            loading: true,
            alerts: {},
            errors: {},
            saved: null,
            saving: null,
        }
        this.alertTypes = [
            {
                name: 'Sub alert',
                type: 'sub',
                minAmount: true,
                canAdd: true,
                vars: [
                    '{twitch_message}',
                    '{user}',
                    '{months}',
                    '{months_streak}',
                    '{plan}',
                ],
            },
            {
                name: 'Sub gift alert',
                type: 'subgift',
                minAmount: false,
                canAdd: false,
                vars: [
                    '{twitch_message}',
                    '{user}',
                    '{to_user}',
                    '{plan}',
                    '{months}',                    
                ],
            },
            {
                name: 'Mystery sub gift',
                type: 'submysterygift',
                minAmount: false,
                canAdd: false,
                vars: [
                    '{twitch_message}',
                    '{user}',
                    '{amount}',
                    '{plan}',
                ],
            },
            {
                name: 'Gifted sub upgraded',
                type: 'giftpaidupgrade',
                minAmount: false,
                canAdd: false,
                vars: [
                    '{twitch_message}',
                    '{user}',
                    '{from_user}',
                ],
            },
            {
                name: 'Sub extended (app)',
                type: 'extendsub',
                minAmount: false,
                canAdd: false,
                vars: [
                    '{twitch_message}',
                    '{months}',
                    '{plan}',
                    '{end_month}',
                    '{end_month_name}',
                ],
            },
        ]
    }

    componentDidMount() {
        setHeader('Chat alerts')
        this.getAlerts()
    }

    getAlerts() {
        api.get(`/api/twitch/channels/${managedUser.id}/chat-alerts`).then(r => {
            this.setState({alerts: r.data, loading: false})
        })
    }

    handleSubmit = (e) => {
        e.preventDefault()
        let t = e.target.dataset.type
        this.setState({saving: t})
        api.put(`/api/twitch/channels/${managedUser.id}/chat-alerts`, {
            [t]: this.state.alerts[t]
        }).then(r => {
            this.setState({
                alerts: r.data, 
                errors: {},
                saved: t,
                saving: null,
            })
        }).catch(e => {
            this.setState({
                errors: {
                    [t]: e.response.data
                }
            })
        })
    }

    handleChange = (e) => {
        if (!(e.target.dataset.type in this.state.alerts))
            this.state.alerts[e.target.dataset.type] = [{}]
        let alerts = this.state.alerts[e.target.dataset.type]
        alerts[e.target.dataset.id][e.target.name] = e.target.value
        this.state.errors = {}
        this.state.saved = null
        this.state.saving = null
        this.setState(this.state)
    }

    handleAdd = (e) => {
        if (!(e.target.dataset.type in this.state.alerts))
            this.state.alerts[e.target.dataset.type] = []
        this.state.alerts[e.target.dataset.type].push({
            message: '',
        })
        this.setState(this.state)        
    }

    handleDelete = (e) => {
        // Since our list items has no ID other than it's index,
        // the render will not pick up on the 
        // So to fix that we just render an empty list and then
        // render the new list.
        let t = e.target.dataset.type
        this.state.alerts[t].splice(e.target.dataset.id, 1)
        let d = this.state.alerts[t]
        this.state.alerts[t] = []
        this.state.errors = {}
        this.state.saving = null
        this.state.saved = null
        this.setState(this.state, () => {
            this.state.alerts[t] = d
            this.forceUpdate()
        })        
    }

    renderType(alertType) {
        let alerts = this.state.alerts[alertType.type] || [{
            message: '',
            min_amount: 0,
        }]
        return <form 
                onSubmit={this.handleSubmit} 
                onChange={this.handleChange} 
                style={{maxWidth:'700px'}}
                data-type={alertType.type}
                className='mb-4'
                key={alertType.type}
            >
                <h2>{alertType.name}</h2>
                <div>Variables: <pre className="mb-0">{alertType.vars.map((val) => {
                    return <span key={'var-'+val}>{val} </span>
                })}</pre></div>
                <div className='d-flex'>
                    <div className='flex-grow-1'>
                        <label>Message</label>
                    </div>
                    {alertType.minAmount?
                    <div className='ml-2'>
                        <label>Months</label>
                    </div>:''}
                    <div style={{width: '48px'}}></div>
                </div>
                {     
                    alerts.map((val, idx) => {
                        return <div className='d-flex mb-2' key={`alert-${alertType.type}-${idx}`}>
                            <div className='flex-grow-1'>
                                <div className='input-group'>
                                    <input 
                                        type='text' 
                                        className='form-control' 
                                        name='message'
                                        data-type={alertType.type}
                                        data-id={idx}
                                        defaultValue={val.message}
                                    />
                                </div>
                            </div>
                            {alertType.minAmount?
                                <div className='ml-2'>
                                    <div className='input-group'>
                                        <input 
                                            style={{width: '100px'}}
                                            type='number' 
                                            className='form-control text-right'
                                            name='min_amount'
                                            data-type={alertType.type}
                                            data-id={idx}
                                            defaultValue={val.min_amount}
                                        />
                                    </div>
                                </div>:''
                            }                            
                            {alertType.canAdd?
                            <div>
                                <button 
                                    title="Delete"
                                    type="button" 
                                    className="btn btn-secondary ml-2"
                                    data-type={alertType.type}
                                    data-id={idx}
                                    onClick={this.handleDelete}
                                >×</button>
                            </div>:''
                            }
                        </div>
                    })
                }

                <SaveButton 
                    isSaving={this.state.saving == alertType.type}
                    isSaved={this.state.saved == alertType.type}
                    savedText='Saved'
                >
                    Save
                </SaveButton>
                
                {alertType.canAdd?
                    <button type="button" className="btn btn-secondary ml-2" data-type={alertType.type} onClick={this.handleAdd}>Add</button>
                    :''
                }

                {renderError(this.state.errors[alertType.type])}
        
        </form>
    }

    render() {
        if (this.state.loading) 
            return <Loading />
        return <>
            {this.alertTypes.map((val) => {
                return this.renderType(val)
            })}
        </>

    }
}

export default ChatAlerts
import React from 'react'
import api from 'tbot/twitch/api'
import Loading from 'tbot/components/loading'

class SelectChannel extends React.Component {

    constructor(props) {
        super(props)
        this.state = {
            channels: [],
            loading: true,
        }
    }

    componentDidMount() {
        this.getChannels()
    }

    getChannels(name) {
        api.get(`/api/twitch/user/admin-of`, {params: {suggest_name: name}}).then(r => {
            this.setState({
                channels: r.data, 
                loading: false
            })
        })
    }

    render() {
        return <div className="modal" tabIndex="-1" role="dialog">
            <div className="modal-dialog" role="document" style={{margin: 0, marginTop: '3.2rem', width:'350px'}}>
                <div className="modal-content" style={{borderRadius:0}}>
                    <div className="modal-header">
                        <h5 className="modal-title">Channels you manage</h5>
                        <button 
                            type="button" 
                            className="close" 
                            data-dismiss="modal" 
                            aria-label="Close" 
                            title="Close"
                            onClick={this.props.onClose}
                        >
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div className="modal-body">
                        <div>
                            <input 
                                className="form-control"
                                placeholder="Search channel"
                                onChange={(e) => {this.getChannels(e.target.value)}}
                            />
                        </div>
                        <div className="mt-2" style={{fontSize: '26px'}}>
                            {this.state.channels.length === 0?<div>No channels found</div>:
                                this.state.channels.map(c => (
                                    <div key={c.id} className="clickable"><a href={`/twitch/${c.name}/dashboard`}>{c.name}</a></div>
                                ))
                            }
                        </div>
                    </div>
                </div>
            </div>
        </div>
    }
}

export default SelectChannel
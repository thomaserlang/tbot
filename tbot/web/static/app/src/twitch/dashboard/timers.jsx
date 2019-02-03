import React from 'react'
import {Link} from 'react-router-dom'
import api from 'tbot/twitch/api'
import Loading from 'tbot/components/loading'
import {setHeader} from 'tbot/utils'
import {userLevelName, enabledWhenName} from 'tbot/twitch/utils'

class Timers extends React.Component {

    constructor(props) {
        super(props)
        this.state = {
            timers: [],
            loading: true,
        }
    }

    componentDidMount() {
        setHeader('Timers')
        this.getTimers()
    }

    getTimers() {        
        api.get(`/api/twitch/channels/${managedUser.id}/timers`).then(r => {
            this.setState({
                timers: r.data, 
                loading: false
            })
        })
    }

    render() {
        if (this.state.loading)
            return <Loading />
        return  <> 
                <div className="d-flex mb-2">
                    <div>
                        <Link className="btn btn-primary" to="timers/new">New timer</Link>
                    </div>
                </div>
                <table className="table table-dark table-hover">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Interval</th>
                        <th title="Enabled when stream is">Enabled status</th>
                        <th title="Enabled">Enabled</th>
                        <th width="5px"></th>
                    </tr>
                </thead>
                <tbody>
                    {this.state.timers.length>0?
                        this.state.timers.map(timer =>
                            <tr key={timer.id}>
                                <td>{timer.name}</td>
                                <td>{timer.interval} minutes</td>
                                <td>{enabledWhenName(timer.enabled_status)}</td>
                                <td>{timer.enabled==1?'Yes':'No'}</td>
                                <td className="text-right"><Link to={`timers/edit/${timer.id}`}>Edit</Link></td>
                            </tr>
                        ): <tr><td colSpan="5" className="text-center">No timers, <Link to="timers/new">create one.</Link></td></tr>
                    }
                </tbody>
            </table>
        </>
    }
}

export default Timers
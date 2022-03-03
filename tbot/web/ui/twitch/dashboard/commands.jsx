import React from 'react'
import {Link} from 'react-router-dom'
import api from 'tbot/twitch/api'
import Loading from 'tbot/components/loading'
import {setHeader} from 'tbot/utils'
import {userLevelName, enabledWhenName} from 'tbot/twitch/utils'

class Commands extends React.Component {

    constructor(props) {
        super(props)
        this.state = {
            commands: [],
            loading: true,
        }
    }

    componentDidMount() {
        setHeader('Commands')
        this.getCommands()
    }

    getCommands() {        
        api.get(`/api/twitch/channels/${managedUser.id}/commands`).then(r => {
            this.setState({
                commands: r.data, 
                loading: false
            })
        })
    }

    render() {
        if (this.state.loading)
            return <Loading />
        return  <div> 
                <div className="d-flex mb-2">
                    <div>
                        <Link className="btn btn-primary" to="commands/new">New command</Link>
                    </div>
                    <div className="ml-auto">
                        <a href={`/t/${managedUser.name}/commands`} target="_blank" className="btn btn-link">Public commands</a>
                    </div>
                </div>
                <table className="table table-dark table-hover">
                <thead>
                    <tr>
                        <th width="100px">Command</th>
                        <th>Response</th>
                        <th width="5px" title="Global cooldown">GCD</th>
                        <th width="5px" title="User cooldown">UCD</th>
                        <th width="100px" title="User level">UL</th>
                        <th width="5px" title="Enabled when stream is">ES</th>
                        <th width="5px" title="Enabled">E</th>
                        <th width="5px"></th>
                    </tr>
                </thead>
                <tbody>                    
                    {this.state.commands.length>0?this.state.commands.map(cmd =>
                        <tr key={cmd.id}>
                            <td>!{cmd.cmd}</td>
                            <td className="td-ellipsis">{cmd.response}</td>
                            <td>{cmd.global_cooldown}</td>
                            <td>{cmd.user_cooldown}</td>
                            <td>{userLevelName(cmd.user_level)}</td>
                            <td>{enabledWhenName(cmd.enabled_status)}</td>
                            <td>{cmd.enabled==1?'Yes':'No'}</td>
                            <td className="text-right"><Link to={`commands/edit/${cmd.id}`}>Edit</Link></td>
                        </tr>
                    ): <tr><td colSpan="8" className="text-center">No commands, <Link to="commands/new">create one.</Link></td></tr>}
                </tbody>
            </table>
        </div>
    }
}

export default Commands
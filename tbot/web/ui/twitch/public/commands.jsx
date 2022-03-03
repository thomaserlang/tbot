import React from 'react'
import {Link} from 'react-router-dom'
import api from 'tbot/twitch/api'
import Loading from 'tbot/components/loading'

class Commands extends React.Component {

    constructor(props) {
        super(props)
        this.state = {
            commands: [],
            loading: true,
        }
    }

    componentDidMount() {
        this.getCommands()
        document.title = `${managedUser.name} - Commands | ${tbot.name}`
    }

    getCommands() {        
        api.get(`/api/twitch/channels/${managedUser.id}/commands-public`).then(r => {
            this.setState({
                commands: r.data, 
                loading: false
            })
        })
    }

    userLevelName(level) {
        switch (level) {
            case 0:
                return ''
                break;
            case 1:
                return 'Subs'
                break;
            case 2:
                return 'VIPs'
                break;
            case 7:
                return 'Mods'
                break;
            case 8:
                return 'Admins'
                break;
            case 9:
                return 'Boradcaster'
                break;
        }
    }

    render() {
        if (this.state.loading)
            return <Loading />
        let groups = []
        for (let cmd of this.state.commands) {
            if (!groups.includes(cmd.group_name))
                groups.push(cmd.group_name)
        }
        let i = 0
        return  <div> 
            <div className="header mt-4">
                <h1 style={{fontSize:'26px'}}>{managedUser.name} - Commands</h1>
            </div>
            {groups.map(group => {
                i++
                return <div key={'group'+i} className="mt-4">
                    <h4>{group}</h4>
                    <table className="table table-dark">
                        <tbody>
                            {this.state.commands.map(cmd => {
                                if (cmd.group_name != group)
                                    return null
                                return <tr key={cmd.id}>
                                    <td width="200px">!{cmd.cmd}</td>
                                    <td>{cmd.response}</td>
                                    <td style={{'textAlign': 'right'}}>{this.userLevelName(cmd.user_level)}</td>
                                </tr>
                            })}
                        </tbody>
                    </table>
                </div>
            })}
        </div>
    }
}

export default Commands
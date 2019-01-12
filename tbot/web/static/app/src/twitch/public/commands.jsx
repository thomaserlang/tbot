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
                return 'Subscribers'
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
        let userLevels = []
        for (let cmd of this.state.commands) {
            if (!(cmd.user_level in userLevels))
                userLevels.push(cmd.user_level)
        }
        return  <div> 
            <div className="header mt-4">
                <h1 style={{fontSize:'26px'}}>{managedUser.name} - Commands</h1>
            </div>

            {userLevels.map(level => 
                <div key={'level'+level} className="mt-4">
                    <h4>{this.userLevelName(level)}</h4>
                    <table className="table table-dark">
                        <tbody>
                            {this.state.commands.map(cmd => {
                                if (cmd.user_level != level)
                                    return null
                                return <tr key={cmd.id}>
                                    <td width="200px">!{cmd.cmd}</td>
                                    <td>{cmd.response}</td>
                                </tr>
                            })}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    }
}

export default Commands
import React from 'react'
import {Link} from 'react-router-dom'
import api from 'tbot/twitch/api'
import Loading from 'tbot/components/loading'
import {setHeader} from 'tbot/utils'

class Admins extends React.Component {

    constructor(props) {
        super(props)
        this.state = {
            admins: [],
            loading: true,
            newAdmin: {
                user: '',
                level: 1
            },
        }
        this.levels = [
            {'name': 'Control commands', 'level': 1},
            {'name': 'Full control', 'level': 3},
        ]
    }

    componentDidMount() {
        setHeader('Admins')
        this.getAdmins()
    }

    getAdmins() {        
        api.get(`/api/twitch/channels/${managedUser.id}/admins`).then(r => {
            this.setState({
                admins: r.data, 
                loading: false
            })
        })
    }
    
    handleNewEvent = (e) => {
        let val = e.target.type === 'checkbox' ? e.target.checked : e.target.value
        this.state.newAdmin[e.target.name] = val
        this.setState({newAdmin: this.state.newAdmin})
    }
    
    handleNewSubmit = (e) => {
        e.preventDefault()
        api.post(`/api/twitch/channels/${managedUser.id}/admins`, this.state.newAdmin).then(r => {
            this.setState({newAdmin: {user: '', level: 1}})
            this.getAdmins()
        }).catch(e => {
            alert(e.response.data.message)
        })
    }

    handleDelete = (admin) => {
        if (!confirm(`Delete ${admin.name}?`))
            return
        api.delete(`/api/twitch/channels/${managedUser.id}/admins/${admin.id}`).then(r => {
            this.getAdmins()
        }).catch(e => {
            alert(e.response.data.message)
        })   
    }

    handleChangeLevel = (e, admin) => {
        api.put(`/api/twitch/channels/${managedUser.id}/admins/${admin.id}`, {
            level: e.target.value,
        }).then(r => {
            this.getAdmins()
        }).catch(e => {
            alert(e.response.data.message)
        }) 
    }

    renderNewAdmin() {
        return <form className="form-inline" onSubmit={this.handleNewSubmit}>
            <div className="form-group">
                <input 
                    className="form-control mr-2" 
                    name="user" 
                    placeholder="User"
                    value={this.state.newAdmin.user}
                    onChange={this.handleNewEvent}
                 />
            </div>
            <select 
                name="level" 
                className="form-control mr-2"
                value={this.state.newAdmin.level}
                onChange={this.handleNewEvent}
            >
                {this.levels.map(l => (
                    <option key={l.level} value={l.level}>{l.name}</option>
                ))}
            </select>
            <button type="submit" className="btn btn-primary">Create</button>
        </form>
    }

    render() {
        if (this.state.loading)
            return <Loading />
        return  <div> 
                <div className="d-flex mb-4">
                    {this.renderNewAdmin()}
                </div>
                <table style={{maxWidth: '500px'}} className="table table-dark table-hover">
                <thead>
                    <tr>
                        <th>User</th>
                        <th width="250px">Level</th>
                        <th width="1px"> </th>
                    </tr>
                </thead>
                <tbody>                    
                    {this.state.admins.length>0?this.state.admins.map(admin =>
                        <tr key={admin.id}>
                            <td className="align-middle">{admin.name}</td>
                            <td>
                                <select 
                                    name="level" 
                                    className="form-control"
                                    value={admin.level}
                                    onChange={(e) => {this.handleChangeLevel(e, admin)}}
                                >
                                    {this.levels.map(l => (
                                        <option key={l.level} value={l.level}>{l.name}</option>
                                    ))}
                                </select>
                            </td>
                            <td className="text-right align-middle">
                                <i 
                                    className="material-icons clickable" 
                                    title="Delete admin"
                                    onClick={() => {this.handleDelete(admin)}}
                                >
                                    delete_forever
                                </i>
                            </td>
                        </tr>
                    ): <tr><td colSpan="3" className="text-center">No admins</td></tr>}
                </tbody>
            </table>
        </div>
    }
}

export default Admins
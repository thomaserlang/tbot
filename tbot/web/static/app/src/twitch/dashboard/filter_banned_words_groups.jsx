import React from 'react'
import {Link} from 'react-router-dom'
import {Redirect} from 'react-router'
import api from 'tbot/twitch/api'
import {setHeader, renderError} from 'tbot/utils'
import Loading from 'tbot/components/loading'
import SaveButton from 'tbot/components/save_button'
import Filter from './components/filter'

class Filter_banned_words_groups extends Filter {

    constructor(props) {
        super(props)
        this.state.groups = []
    }

    componentDidMount() {
        setHeader('Banned words groups')
        this.getFilters()
    }

    getFilters() {
        this.setState({loading: true})
        api.get(`/api/twitch/channels/${managedUser.id}/filters/banned-words-groups`).then(r => {
            this.setState({
                loading: false,
                groups: r.data,
            })
        })
    }
    
    render() {
        if (this.state.loading)
            return <Loading text="Loading filter" />
        return <>
            <div className="d-flex mb-2">
                <div>
                    <Link className="btn btn-primary" to="banned-words/new">New group</Link>
                </div>
            </div>
            <table className="table" style={{width:'500px'}}>
                <tbody>
                {this.state.groups.length > 0?
                    this.state.groups.map((group, idx) =>
                        <tr key={group.id}>
                            <td><Link to={`banned-words/edit/${group.id}`}>{group.name}</Link></td>
                        </tr>
                    ):
                    <tr><td colSpan="8" className="text-center">
                        No groups, <Link to="banned-words/new">create one.</Link>
                    </td></tr>
                }
                </tbody>
            </table>
        </>
    }

}

export default Filter_banned_words_groups
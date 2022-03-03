import React from 'react'
import {Link} from 'react-router-dom'
import api from 'tbot/twitch/api'
import {setHeader} from 'tbot/utils'
import Loading from 'tbot/components/loading'

import './filters.scss'

class Filters extends React.Component {

    constructor(props) {
        super(props)
        this.state = {
            loading: true,
            filters: {},
        }
        this.filters = [
            {
                'title': 'Link filter',
                'type': 'link',
                'desc': 'Remove links in chat.',
            },
            {
                'title': 'Paragraph filter',
                'type': 'paragraph',
                'desc': 'Remove long messages.',
            },
            {
                'title': 'Symbol filter',
                'type': 'symbol',
                'desc': 'Remove excessive use of symbols.',
            },
            {
                'title': 'Caps filter',
                'type': 'caps',
                'desc': 'Remove excessive use of caps.',
            },
            {
                'title': 'Emote filter',
                'type': 'emote',
                'desc': 'Remove excessive use of emotes.',
            },
            {
                'title': 'Non-latin filter',
                'type': 'non-latin',
                'desc': 'Remove non-latin text',
            },
            {
                'title': 'Action filter',
                'type': 'action',
                'desc': 'Remove colored /me text',
            },
        ]
    }

    componentDidMount() {
        setHeader('Filters')
        this.getFilters()
    }

    getFilters() {
        api.get(`/api/twitch/channels/${managedUser.id}/filters`).then(r => {
            this.setState({
                loading: false,
                filters: r.data,
            })
        })
    }

    render() {
        if (this.state.loading)
            return <Loading text="Loading filters" />
        return <div id="filters" className="d-flex flex-wrap">
            {this.filters.map(f => (
                <Link key={f.type} to={`/twitch/${managedUser.name}/filters/${f.type}`}>
                    <div className="filter">
                        <div className="title">{f.title}</div>
                        <div className="description">{f.desc}</div>
                        <div className="status">
                            {(f.type in this.state.filters && this.state.filters[f.type].enabled)?
                                <strong className="text-success">Enabled</strong>:
                                <span className="text-info">Not enabled</span>
                            }
                        </div>
                    </div>
                </Link>
            ))}
        </div>
    }

}

export default Filters
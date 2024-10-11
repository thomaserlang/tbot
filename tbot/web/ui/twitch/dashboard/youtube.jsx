import React from 'react'
import Loading from 'tbot/components/loading'
import api from 'tbot/twitch/api'
import { setHeader } from 'tbot/utils'

class YouTube extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            loading: true,
            youtube: {},
            connecting: false,
            deleting: false,
        }
    }

    componentDidMount() {
        setHeader('YouTube')
        this.getStatus()
    }

    getStatus() {
        this.setState({ loading: true })
        api.get(`/api/twitch/channels/${managedUser.id}/youtube`).then((r) => {
            this.setState({ youtube: r.data, loading: false })
        })
    }

    handleSubmit = () => {
        this.setState({ connecting: true })
    }

    handleDelete = (e) => {
        e.preventDefault()
        this.setState({ deleting: true })
        api.delete(`/api/twitch/channels/${managedUser.id}/youtube`).then(
            (r) => {
                this.setState({ youtube: {}, deleting: false })
            }
        )
    }

    render() {
        if (this.state.loading) return <Loading />
        if (this.state.youtube.connected)
            return (
                <div>
                    <div className="mb-3">
                        Connected to YouTube account:{' '}
                        {this.state.youtube.handle}
                    </div>
                    <form method="post" onSubmit={this.handleDelete}>
                        <button type="submit" className="btn btn-danger">
                            Disconnect YouTube
                        </button>
                    </form>
                </div>
            )
        return (
            <div>
                <form
                    method="post"
                    onSubmit={this.handleSubmit}
                    action={`/api/twitch/channels/${managedUser.id}/youtube`}
                >
                    <button type="submit" className="btn btn-success">
                        Connect YouTube
                    </button>
                </form>
            </div>
        )
    }
}

export default YouTube

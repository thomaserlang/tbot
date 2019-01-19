import React from 'react'
import api from 'tbot/twitch/api'

class ExtraAuth extends React.Component {

    constructor(props) {
        super(props)
        this.state = {
            loading: true,
            data: null,
        }
    }

    componentDidMount() {
        this.getData()
    }

    getData() {
        api.get(`/api/twitch/channels/${managedUser.id}/check-extra-auth`).then(r => {
            this.setState({data: r.data, 'loading': false})
        })
    }

    render() {
        console.log(this.state.loading)
        if (this.state.loading)
            return null
        if (this.state.data.has_extra_auth)
            return null
        return <div className="box mr-3" style={{width: '400px'}}>
            <div className="title">Extra authorization needed</div>
            <div className="content">
                For the bot to be able to change title, game category and 
                read subscribers, extra authorization is needed.

                <div className="d-flex mt-3 mb-3">
                    <div className="ml-auto mr-auto">
                        <a 
                            href="/twitch/login?request_extra_auth=true"
                            className="btn btn-success"
                        >
                            Give extra authorization
                        </a>
                    </div>
                </div>
            </div>
        </div>
    }
}

export default ExtraAuth
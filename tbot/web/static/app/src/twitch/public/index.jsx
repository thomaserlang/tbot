import React from 'react'
import {Route, Redirect} from "react-router-dom"
import {renderError} from 'tbot/utils'
import api from 'tbot/twitch/api'
import Loading from 'tbot/components/loading'
import Commands from './commands'

class Main extends React.Component {

    render() {
        if (this.state.loading) {
            this.getChannel()
            return <Loading text="LOADING" />
        }
        if (this.state.error) {
            return <div className="mt-5 ml-auto mr-auto" style={{width: '600px'}}>
                {renderError(this.state.error)}
            </div>
        }
        return <div className="container">
            <Route exact path='/twitch/c/:channel/commands' component={Commands}/>
        </div>
    }

    constructor(props) {
        super(props)
        this.state = {
            loading: true,
            errors: null,
        }
    }

    componentDidUpdate(prevProps) {
        if (this.props.location !== prevProps.location) {
            window.scrollTo(0, 0)
        }
    }

    getChannel() {
        window.managedUser = null
        api.get(`/api/twitch/channel/${this.props.match.params.channel}`).then(r => {
            window.managedUser = r.data
            this.setState({loading: false})
        }).catch(e => {
            this.setState({loading: false, error: e.response.data})
        })
    }

}

export default Main
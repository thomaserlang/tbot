import React from 'react'
import {Route, Redirect} from "react-router-dom"
import {requireAuth} from 'tbot/twitch/utils'
import {renderError} from 'tbot/utils'
import api from 'tbot/twitch/api'
import Loading from 'tbot/components/loading'
import Sidebar from './components/sidebar'
import Topbar from './components/topbar'
import Dashboard from './dashboard'
import Commands from './commands'
import Command from './command'
import Spotify from './spotify'
import Discord from './discord'
import Admins from './admins'
import Filters from './filters'
import Filter_link from './filter_link'
import Filter_paragraph from './filter_paragraph'
import Filter_symbol from './filter_symbol'
import Filter_caps from './filter_caps'
import Filter_emote from './filter_emote'
import Filter_non_latin from './filter_non_latin'
import Filter_action from './filter_action'
import Filter_banned_words_groups from './filter_banned_words_groups'
import Filter_banned_words from './filter_banned_words'
import Timers from './timers'
import Timer from './timer'
import ChatAlerts from './chat_alerts'
import PointsSettings from './points_settings'
import GamblingSlotsSettings from './gambling_slots_settings'
import GamblingRouletteSettings from './gambling_roulette_settings'

class Main extends React.Component {

    render() {
        if (!this.props.match.params.channel) 
            return <Redirect to={`/twitch/${window.tbot.twitch_user.user}/dashboard`} />
        if (this.state.loading) {
            this.getChannel()
            return <Loading text="LOADING" />
        }
        if (this.state.error) {
            return <div className="mt-5 ml-auto mr-auto" style={{width: '600px'}}>
                {renderError(this.state.error)}
            </div>
        }
        return <div id="main-wrapper">
            <Sidebar />
            <div id="content-wrapper">
                <Topbar />
                <div id="content">
                    <Route exact path='/twitch/:channel/dashboard' component={Dashboard}/>
                    <Route exact path='/twitch/:channel/commands' component={Commands}/>
                    <Route exact path='/twitch/:channel/commands/edit/:id' component={Command}/>
                    <Route exact path='/twitch/:channel/commands/new' component={Command}/>
                    <Route exact path='/twitch/:channel/spotify' component={Spotify}/>
                    <Route exact path='/twitch/:channel/discord' component={Discord}/>
                    <Route exact path='/twitch/:channel/admins' component={Admins}/>
                    <Route exact path='/twitch/:channel/filters' component={Filters}/>
                    <Route exact path='/twitch/:channel/filters/link' component={Filter_link}/>
                    <Route exact path='/twitch/:channel/filters/paragraph' component={Filter_paragraph}/>
                    <Route exact path='/twitch/:channel/filters/symbol' component={Filter_symbol}/>
                    <Route exact path='/twitch/:channel/filters/caps' component={Filter_caps}/>
                    <Route exact path='/twitch/:channel/filters/emote' component={Filter_emote}/>
                    <Route exact path='/twitch/:channel/filters/non-latin' component={Filter_non_latin}/>
                    <Route exact path='/twitch/:channel/filters/action' component={Filter_action}/>
                    <Route exact path='/twitch/:channel/banned-words' component={Filter_banned_words_groups}/>
                    <Route exact path='/twitch/:channel/banned-words/edit/:id' component={Filter_banned_words}/>
                    <Route exact path='/twitch/:channel/banned-words/new' component={Filter_banned_words}/>
                    <Route exact path='/twitch/:channel/timers' component={Timers}/>
                    <Route exact path='/twitch/:channel/timers/edit/:id' component={Timer}/>
                    <Route exact path='/twitch/:channel/timers/new' component={Timer}/>
                    <Route exact path='/twitch/:channel/chat-alerts' component={ChatAlerts}/>
                    <Route exact path='/twitch/:channel/points-settings' component={PointsSettings} />
                    <Route exact path='/twitch/:channel/gambling-slots-settings' component={GamblingSlotsSettings} />
                    <Route exact path='/twitch/:channel/gambling-roulette-settings' component={GamblingRouletteSettings} />
                </div>
            </div>
        </div>
    }

    constructor(props) {
        super(props)
        requireAuth()
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
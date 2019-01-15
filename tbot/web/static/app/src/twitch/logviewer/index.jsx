import React from 'react'
import {Link} from 'react-router-dom'
import api from 'tbot/twitch/api'
import qs from 'query-string'
import moment from 'moment'
import {setTitle} from 'tbot/utils'
import Loading from 'tbot/components/loading'
import UserInput from './userinput'
import './logviewer.scss'
import '../dashboard/components/topbar.scss'

class Logviewer extends React.Component {

    constructor(props) {
        super(props)
        this.query = qs.parse(location.search)
        this.state = {
            channel: null,
            loading: true,
            chatlog: [],
            loading: true,
            loadingChannel: true,
            userChatStats: null,
            showLoadBefore: false,
            showLoadAfter: true,
            accessDenied: false,
        }
        this.loadBefore = this.loadBefore.bind(this);
        this.loadAfter = this.loadAfter.bind(this);
    }

    componentDidMount() {
        let channel = this.props.match.params.channel;
        setTitle(`${channel} | Twitch Logviewer`)
        api.get(`/api/twitch/channels`, {params: {name:channel}}).then(data => {
            this.setState({
                channel: data.data[0],
                loadingChannel: false,
            }, state => {
                this.loadChatlog({
                    before_id: this.query.before_id,
                })
                this.loadUserChatStats()
            })
        })
    }

    loadChatlog(params) {
        this.setState({loading: true})
        params['user'] = this.query.user
        params['message'] = this.query.message
        params['show_mod_actions_only'] = this.query.show_mod_actions_only
        api.get(`/api/twitch/channels/${this.state.channel.id}/chatlog`, {params: params}).then(r => {
            let l = this.state.chatlog;
            if ('after_id' in params)                
                l.push(...r.data)
            else
                l.unshift(...r.data);
            if ('after_id' in params) {
                this.state.showLoadAfter = r.data.length == r.headers['x-per-page']
            } else {
                this.state.showLoadBefore = r.data.length == r.headers['x-per-page'] 
                if (this.state.showLoadAfter != false) {
                    this.state.showLoadAfter = (this.query.before_id);
                }
            }
            this.setState({
                loading: false,
                chatlog: l,
            })
        }).catch(e => {
            if (e.response.status == 403) {
                this.setState({
                    accessDenied: true,
                })
            }
        })
    }

    loadBefore(e) {
        e.preventDefault();
        this.loadChatlog({
            before_id: this.state.chatlog[0].id,
        })
    }

    loadAfter(e) {
        e.preventDefault();
        this.loadChatlog({
            after_id: this.state.chatlog[this.state.chatlog.length-1].id,
        })
    }

    loadUserChatStats() {
        this.setState({
            userChatStats: null,
            loading: true,
        })
        if (!this.query.user)
            return
        api.get(`/api/twitch/channels/${this.state.channel.id}/user-chatstats`, {params: {
            user: this.query.user,
        }}).then(r => {
            this.setState({
                userChatStats: r.data,
                loading: false,
            })
        })   
    }

    renderChatlog() {
        if (this.state.chatlog.length == 0)
            if (this.state.loading)
                return <Loading text="LOADING" />
            else
                return <div className="m-2"><center>No results found</center></div>
        return <table className="chatlog table table-dark table-striped table-sm table-hover">
            <tbody>
                {this.state.showLoadBefore?
                    <tr><td colSpan="3" style={{textAlign: 'center'}}>
                        {this.state.loading?
                            <div class="spinner-grow text-primary" role="status"></div>:
                            <a href="#" onClick={this.loadBefore}>Load more</a>}
                        </td></tr>
                : null}
                {this.state.chatlog.map(l => (
                    <tr key={l.id}>
                        <td 
                            width="10px"
                            dateTime={l.created_at}
                            style={{whiteSpace:'nowrap'}}
                        >
                            <a href={`?before_id=${l.id+1}`}>{this.iso8601toLocalTime(l.created_at)}</a>
                        </td>
                        <td width="10px"><a href={`?user=${l.user}`}>{l.user}</a></td>
                        <td>
                            {this.renderTypeSymbol(l)}
                            {l.message} 
                        </td>
                    </tr>
                ))}                
                {this.state.showLoadAfter?
                    <tr><td colSpan="3" style={{textAlign: 'center'}}>
                        {this.state.loading?
                            <div class="spinner-grow text-primary" role="status"></div>:
                            <a href="#" onClick={this.loadAfter}>Load more</a>}
                        </td></tr>
                : null}
            </tbody>
        </table>
    }

    renderTypeSymbol(l) {
        switch(l.type) {
            case 2:
                return <span className="badge badge-danger">B</span>
                break;
            case 3:
                return <span className="badge badge-warning">T</span> 
                break;
            case 4:
                return <span className="badge badge-info">P</span> 
                break;
            case 100:
                return <span className="badge badge-success">M</span> 
                break;
            default:
                return null
                break;
        }
    }

    iso8601toLocalTime(t) {
        let date = moment(t);
        return date.format('YYYY-MM-DD HH:mm:ss')
    }

    renderUserStats() {
        if (this.state.userChatStats == null)
            return null

        return <div className="userChatStats">
            <span><b>Total messages:</b> {this.state.userChatStats.chat_messages||0}</span>
            <span><b>Purges:</b> {this.state.userChatStats.purges||0}</span>
            <span><b>Timeouts:</b> {this.state.userChatStats.timeouts||0}</span>
            <span><b>Bans:</b> {this.state.userChatStats.bans||0}</span>
        </div>

    }

    renderAccessDenied() {
        return <div className="access-denied">
            Sorry,
            <br />
            you must be a moderator to view the chatlog of this channel
        </div>
    }

    render() {
        if (this.state.loadingChannel)
            return <Loading text="LOADING" />
        if (this.state.accessDenied)
            return this.renderAccessDenied()
        return <div id="logviewer">
            <div id="topbar" style={{'border': 'none', 'borderBottom': '1px solid #000', 'padding-left': '0.5rem', 'padding-left': '0.5rem'}}>
                <div className="title" id="top-title">
                    <Link to="/twitch/logviewer" className="text-white">
                        <i className="material-icons material-inline ">arrow_back</i></Link> Logviewer for {this.state.channel.name}
                </div>
                <div className="signed-as">Signed in as <b>{tbot['twitch_user']['user']}</b>, <a href="/twitch/logout">log out</a></div>
            </div>
            <div className="sticky-top">
                <div className="filter">
                    <form className="form-inline">
                        <UserInput defaultValue={this.query.user} channel_id={this.state.channel.id} />
                        <input 
                            name="message" 
                            type="text" 
                            className="form-control" 
                            placeholder="Message"
                            defaultValue={this.query.message}
                        />
                        <button type="submit" className="btn btn-warning">Search</button>
                        <input 
                            type="checkbox" 
                            value="yes" 
                            name="show_mod_actions_only" 
                            className="form-check-input" 
                            id="show_mod_actions_only" 
                            defaultChecked={this.query.show_mod_actions_only=='yes'}
                        />
                        <label className="form-check-label" htmlFor="show_mod_actions_only">Show only mod actions</label>
                    </form>
                </div>
                {this.renderUserStats()}
            </div>
            {this.renderChatlog()}
        </div>;
    }

}

export default Logviewer
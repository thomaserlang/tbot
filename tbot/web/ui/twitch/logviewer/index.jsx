import React from 'react'
import {Link} from 'react-router-dom'
import api from 'tbot/twitch/api'
import qs from 'query-string'
import {setTitle, iso8601toLocalTime} from 'tbot/utils'
import Loading from 'tbot/components/loading'
import UserInput from './userinput'
import UserStats from './user_stats'
import UserStreamsWatched from './user_streams_watched'
import UserAKAs from './user_akas'
import './logviewer.scss'
import '../dashboard/components/topbar.scss'

class Logviewer extends React.Component {

    constructor(props) {
        super(props)
        this.query = qs.parse(location.search)
        this.state = {
            channel: null,
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
            })
        })
    }

    loadChatlog(params) {
        this.setState({loading: true})
        params['user'] = this.query.user
        params['message'] = this.query.message
        params['show_mod_actions_only'] = this.query.show_mod_actions_only
        api.get(`/api/twitch/channels/${this.state.channel.id}/chatlog`, {params: params}).then(r => {
            const l = [...this.state.chatlog];
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
                chatlog: l,
            })
        }).catch(e => {
            if (e.response.status == 403) {
                this.setState({
                    accessDenied: true,
                })
            }
        }).finally(() => {
            this.setState({loading: false})
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

    renderChatlog() {
        if (this.state.chatlog.length == 0) { 
            if (this.state.loading)
                return <div className="chatlog">
                        <h3>Chat logs</h3>
                        <div className="spacing">Loading chat logs...</div>
                    </div>
                
            return <div className="chatlog">
                <h3>Chat logs</h3>
                <div className="spacing">No chat logs found</div>
            </div>
        }
        
        return <div className="chatlog">
                <h3>Chat logs</h3>        
                <table className="table table-dark table-sm table-hover">
                <tbody>
                    {this.state.showLoadBefore?
                        <tr><td colSpan="3" style={{textAlign: 'center'}}>
                            {this.state.loading?
                                <div className="spinner-grow text-primary" role="status"></div>:
                                <a href="#" onClick={this.loadBefore}>Load more chat logs</a>}
                            </td></tr>
                    : null}
                    {this.state.chatlog.map(l => (
                        <tr key={l.id}>
                            <td 
                                width="10px"
                                dateTime={l.created_at}
                                style={{whiteSpace:'nowrap'}}
                            >
                                <a href={`?before_id=${l.id+1}`}>{iso8601toLocalTime(l.created_at)}</a>
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
                                <div className="spinner-grow text-primary" role="status"></div>:
                                <a href="#" onClick={this.loadAfter}>Load more chat logs</a>}
                            </td></tr>
                    : null}
                </tbody>
            </table>
        </div> 
    }

    renderTypeSymbol(l) {
        switch(l.type) {
            case 2:
                return <span className="badge badge-primary">S</span>
                break;
            case 100:
                return <span className="badge badge-success">M</span> 
                break;
            default:
                return null
                break;
        }
    }




    viewMoreClick = (e) => {
        e.preventDefault()
        
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
            <div id="topbar" style={{'border': 'none', 'borderBottom': '1px solid #000', 'paddingLeft': '0.5rem'}}>
                <div className="title" id="top-title">
                    <Link to="/twitch/logviewer" className="text-white">
                        <i className="material-icons material-inline ">arrow_back</i></Link> Logviewer for {this.state.channel.name}
                </div>
                {tbot.twitch_user?
                <div className="signed-as">Signed in as <b>{tbot.twitch_user.user}</b>, <a href="/twitch/logout">log out</a></div>
                :null}
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
                {this.query.user?<UserStats channelId={this.state.channel.id} user={this.query.user} />: null}
            </div>
            
            {this.renderChatlog()}

            {this.query.user?<UserStreamsWatched channelId={this.state.channel.id} user={this.query.user} />: null}
            
            {this.query.user?<UserAKAs channelId={this.state.channel.id} user={this.query.user} />: null}

        </div>;
    }

}

export default Logviewer
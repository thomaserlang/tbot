import React from 'react'
import api from 'tbot/twitch/api'

class Commercial extends React.Component {
    state = {
        retry_at: 0,
    }

    componentWillUnmount() {
        clearInterval(this.retryTimer);
      }

    startAd = (e) => {
        e.preventDefault()
        let length = parseInt(e.target.dataset.length)
        api.post(`/api/twitch/channels/${managedUser.id}/commercial`, {
            'length': length,
        }).then(r => {
            this.setState({
                retry_at: (Math.floor(new Date().getTime() / 1000)) + r.data.retry_after,
            })
            this.retryTimer = setInterval(() => this.forceUpdate(), 1000)
        }).catch(e => {
            alert(e.response.data.message)
            if (!e.response.data.extra?.retry_after) {
                this.setState({
                    retry_at: (Math.floor(new Date().getTime() / 1000)) + e.response.data.extra.retry_after,
                })
                this.retryTimer = setInterval(() => this.forceUpdate(), 1000)
            }
        })
    }

    render() {
        if (managedUser.level < 3)
            return null 
        const now = Math.floor(new Date().getTime() / 1000)
        if (this.state.retry_at && (now < this.state.retry_at)){
            return <div className="box mt-3">
                <div className="title">Commercial</div>
                <div className="buttons">
                    <button className="btn btn-secondary" disabled>
                        Wait {this.state.retry_at-now} seconds
                    </button>
                </div>
            </div>
        } else {            
            clearInterval(this.retryTimer);
        }

        return <div className="box mt-3">
            <div className="title">Commercial</div>
            <div className="buttons">
                <button className="btn btn-secondary" onClick={this.startAd} data-length="30">30 seconds</button>
                <button className="btn btn-secondary" onClick={this.startAd} data-length="60">1 minute</button>
                <button className="btn btn-secondary" onClick={this.startAd} data-length="90">1.5 minute</button>
                <button className="btn btn-secondary" onClick={this.startAd} data-length="120">2 minutes</button>
                <button className="btn btn-secondary" onClick={this.startAd} data-length="180">3 minutes</button>
            </div>
        </div>
    }
}

export default Commercial
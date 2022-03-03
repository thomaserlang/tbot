import React from 'react'

class WebSocketBase extends React.Component {

    constructor(props) {
        super(props)
        this.connect()        
        this.pingTimer = setInterval(this.ping, 20000)
        this.pongTimer = null
    }

    connect() {
        clearTimeout(this.pongTimer)
        this.pongTimer = null
        if (this.socket !== undefined && (this.socket && this.socket.readyState === 1))
            this.socket.close()
        this.socket = new WebSocket(((window.location.protocol === "https:") ? "wss://" : "ws://") + window.location.host + "/api/twitch/widget-ws")
        this.socket.onopen = this.onOpen
        this.socket.onmessage = this.onMessage
        this.socket.onclose = this.onClose
    }

    send(data) {
        this.socket.send(JSON.stringify(data))
    }

    onOpen = (event) => {
        this.send({
            'type': 'LISTEN',
            'data': {
                'key': window.key,
            }
        })
    }

    onMessage = (event) => {
        let data = JSON.parse(event.data)
        if (data.type == 'PONG') {
            clearTimeout(this.pongTimer)
            this.pongTimer = null
        }
    }

    onClose = (event) => {
        if (!this.pongTimer) 
            this.pongTimer = setTimeout(() => this.connect(), 5000)
    }

    ping = () => {
        if (!this.pongTimer)
            this.pongTimer = setTimeout(() => this.connect(), 5000)
        this.send({'type': 'PING'})
    }
}

export default WebSocketBase
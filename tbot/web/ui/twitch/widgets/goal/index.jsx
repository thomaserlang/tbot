import WebSocketBase from '../websocket_base'
import ReactDOM from "react-dom"

class GoalWidget extends WebSocketBase {

    componentDidMount() {
        
    }

    render() {
        return <div>
            Test
        </div>
    }
}

ReactDOM.render(<GoalWidget />,
    document.getElementById("root")
)

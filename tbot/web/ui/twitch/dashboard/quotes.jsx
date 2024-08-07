import React from 'react'
import {Link} from 'react-router-dom'
import api from 'tbot/twitch/api'
import Loading from 'tbot/components/loading'
import {setHeader} from 'tbot/utils'

class Quotes extends React.Component {

    constructor(props) {
        super(props)
        this.state = {
            quotes: [],
            loading: true,
        }
    }

    componentDidMount() {
        setHeader('Quotes')
        this.getQuotes()
    }

    getQuotes() {        
        api.get(`/api/twitch/channels/${managedUser.id}/quotes`).then(r => {
            this.setState({
                quotes: r.data, 
                loading: false
            })
        })
    }

    render() {
        if (this.state.loading)
            return <Loading />
        return  <div> 
                <table className="table table-dark table-hover">
                <thead>
                    <tr>
                        <th width="5px">Number</th>
                        <th>Quote</th>
                    </tr>
                </thead>
                <tbody>                    
                    {this.state.quotes.length>0?this.state.quotes.map(quote =>
                        <tr key={quote.number}>
                            <td>{quote.number}</td>
                            <td>{quote.message}</td>
                            <td className="text-right"><Link to={`quotes/edit/${quote.id}`}>Edit</Link></td>
                        </tr>
                    ): <tr><td colSpan="8" className="text-center">No quotes.</td></tr>}
                </tbody>
            </table>
        </div>
    }
}

export default Quotes
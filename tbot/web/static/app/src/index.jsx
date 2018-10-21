import ReactDOM from 'react-dom';
import {BrowserRouter, Switch, Route} from "react-router-dom";

import Logviewer from 'tbot/twitch/logviewer';
import SelectChannel from 'tbot/twitch/logviewer/selectchannel';
import Sidebar from 'tbot/sidebar';
import Front from 'tbot/front'

import './index.scss';

ReactDOM.render((
    <BrowserRouter>
        <Switch>
            <Route exact path='/' component={Front}/>
            <Route exact path='/twitch/logviewer' component={SelectChannel}/>
            <Route exact path='/twitch/logviewer/:channel' component={Logviewer}/>
        </Switch>
    </BrowserRouter>
), document.getElementById('root'));
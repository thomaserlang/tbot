import ReactDOM from "react-dom";
import { BrowserRouter, Switch, Route } from "react-router-dom";

import Front from "tbot/front";
import LiveChat from "tbot/live_chat";

import TwitchLogviewer from "tbot/twitch/logviewer";
import TwitchLogViewerSelectChannel from "tbot/twitch/logviewer/selectchannel";

import TwitchDashboard from "tbot/twitch/dashboard";

import TwitchPublic from "tbot/twitch/public";

import "./index.scss";

ReactDOM.render(
  <BrowserRouter>
    <Switch>
      <Route exact path="/" component={Front} />

      <Route exact path="/live-chat/:channelId" component={LiveChat} />

      <Route
        exact
        path="/twitch/logviewer"
        component={TwitchLogViewerSelectChannel}
      />
      <Route
        exact
        path="/twitch/logviewer/:channel"
        component={TwitchLogviewer}
      />

      <Route path="/t/:channel" component={TwitchPublic} />

      <Route path="/twitch/dashboard" component={TwitchDashboard} />
      <Route path="/twitch/:channel" component={TwitchDashboard} />
    </Switch>
  </BrowserRouter>,
  document.getElementById("root")
);

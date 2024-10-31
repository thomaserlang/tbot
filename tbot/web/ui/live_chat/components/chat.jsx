import React, { useState, useEffect, useRef } from "react";
import { parseEmotes } from "emotettv";
import useWebSocket from "react-use-websocket";
import { RenderMessage } from "./render_message";
import { RenderModAction } from "./render_mod_action";
import { RenderNotice } from "./render_notice";
import { parseTwitchEmotes, parseTwitchBadges } from "../parse_tags";
import { useParseEmotes } from "./parse_emotes";

import "./chat.scss";

export function Chat({ channelId }) {
  const { lastJsonMessage } = useWebSocket(`/api/live-chat/${channelId}`, {
    shouldReconnect: () => true,
  });
  const [messageHistory, setMessageHistory] = useState([]);
  const messagesEndRef = useRef(null);
  const { parseEmoteMessage } = useParseEmotes({ channelId });

  useEffect(() => {
    if (lastJsonMessage === null) return;

    const parse = async () => {
      const msg = { ...lastJsonMessage };
      if (msg.provider === "twitch") {
        parseTwitchEmotes(msg);
        parseTwitchBadges(msg);

        // emotettv.parseEmotes keeps fetching all emotes on each message
        // only use it for twitch emotes since they are parsed directly.
        msg.message = (
          await parseEmotes(parseEmoteMessage(msg.message), msg.emotes, {
            channelId: channelId,
            providers: {
              ffz: false,
              bttv: false,
              seventv: false,
              twitch: true,
            },
          })
        ).toHTML(1, true, false);
      } else {
        msg.message = parseEmoteMessage(msg.message);
      }
      setMessageHistory((prevMessages) => {
        const updatedMessages = [...prevMessages, msg];
        return updatedMessages.slice(-500);
      });
    };
    parse();
  }, [lastJsonMessage]);

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "instant" });
    }
  }, [messageHistory]);

  return (
    <div className="chat-container">
      <div className="messages">
        {messageHistory.map((msg) => (
          <RenderMsg key={msg.id} msg={msg} />
        ))}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
}

function RenderMsg({ msg }) {
  if (msg.type == "message") {
    return <RenderMessage msg={msg} />;
  }
  if (msg.type == "mod_action") {
    return <RenderModAction msg={msg} />;
  }
  if (msg.type == "notice") {
    return <RenderNotice msg={msg} />;
  }
}

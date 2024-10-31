import React, { useState, useEffect, useRef } from "react";
import { parseBadges, parseEmotes } from "emotettv";
import useWebSocket from "react-use-websocket";
import { RenderMessage } from "./render_message";
import { RenderModAction } from "./render_mod_action";
import { RenderNotice } from "./render_notice";
import { parseTwitchEmotes, parseTwitchBadges } from "../parse_tags";

import "./chat.scss";

export function Chat({ channelId }) {
  const { lastJsonMessage } = useWebSocket(`/api/live-chat/${channelId}`, {
    shouldReconnect: () => true,
  });
  const [messageHistory, setMessageHistory] = useState([]);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    if (lastJsonMessage === null) return;

    const parse = async () => {
      const msg = { ...lastJsonMessage };
      if (msg.provider === "twitch") {
        parseTwitchEmotes(msg);
        parseTwitchBadges(msg);
        msg.badgesHTML = (await parseBadges(msg.badges, msg.user)).toHTML();
        msg.message = (
          await parseEmotes(msg.message, msg.emotes, { channelId: channelId })
        ).toHTML();
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

import React, { useState, useEffect, useRef } from "react";
import { useParseEmotes } from "./parse_emotes";
import useWebSocket from "react-use-websocket";
import sanitizeHtml from "sanitize-html";
import "./chat.scss";

export function Chat({ channelId }) {
  const { lastJsonMessage } = useWebSocket(`/api/live-chat/${channelId}`, {
    shouldReconnect: () => true,
  });
  const [messageHistory, setMessageHistory] = useState([]);
  const messagesEndRef = useRef(null);
  const { parseEmoteMessage } = useParseEmotes({ channelId });

  useEffect(() => {
    if (lastJsonMessage !== null) {
      setMessageHistory((prevMessages) => {
        const updatedMessages = [...prevMessages, lastJsonMessage];
        return updatedMessages.slice(-500);
      });
    }
  }, [lastJsonMessage]);

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "instant" });
    }
  }, [messageHistory]);

  return (
    <div className="chat-container">
      <div className="messages">
        {messageHistory.map((msg, index) => (
          <div key={index} className="message">
            <div className="time">
              {new Date(msg.created_at).toLocaleTimeString([], {
                hour: "2-digit",
                minute: "2-digit",
                hour12: false,
              })}
            </div>
            {providerShort(msg.provider)}
            <div>
              <span className="username" style={{ color: msg.user_color }}>
                {msg.user}
              </span>
              :
            </div>

            <div
              className="text"
              dangerouslySetInnerHTML={{
                __html: sanitizeHtml(parseEmoteMessage(msg.message), {
                  allowedTags: ["img"],
                  allowedAttributes: {
                    img: ["src", "title", "class"],
                  },
                }),
              }}
            ></div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
}

function providerShort(provider) {
  switch (provider) {
    case "twitch":
      return (
        <span className="provider twitch" title="Twitch">
          T
        </span>
      );
    case "youtube":
      return (
        <span className="provider youtube" title="YouTube">
          Y
        </span>
      );
  }
}

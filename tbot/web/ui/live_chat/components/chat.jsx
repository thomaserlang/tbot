import React, { useState, useEffect, useRef } from "react";
import useWebSocket, { ReadyState } from "react-use-websocket";
import "./chat.scss";

export function Chat({ channelId }) {
  const {
    sendMessage,
    sendJsonMessage,
    lastMessage,
    lastJsonMessage,
    readyState,
    getWebSocket,
  } = useWebSocket(`/api/live-chat/${channelId}`, {
    onOpen: () => console.log("opened"),
    shouldReconnect: (closeEvent) => true,
  });
  const [messageHistory, setMessageHistory] = useState([]);
  const messagesEndRef = useRef(null);

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
  console.log(lastJsonMessage);
  return (
    <div className="chat-container">
      <div className="messages">
        {messageHistory.map((msg, index) => (
          <div key={index} className="message">
            {providerShort(msg.provider)}
            <span className="username" style={{ color: msg.color }}>
              {msg.user}
            </span>
            : <span className="text">{msg.message}</span>
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
      return <span className="provider twitch">T</span>;
    case "youtube":
      return <span className="provider youtube">Y</span>;
  }
}

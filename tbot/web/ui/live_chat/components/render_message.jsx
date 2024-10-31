import React from "react";
import sanitizeHtml from "sanitize-html";
import { providerShort } from "./provider_short";
import "./chat.scss";

export function RenderMessage({ msg }) {
  return (
    <div className="message">
      <span className="time">
        {new Date(msg.created_at).toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
          hour12: false,
        })}
      </span>
      {providerShort(msg.provider)}
      <span className="username" style={{ color: fixColor(msg.user_color) }}>
        {msg.user}
      </span>
      :
      <span
        className="text"
        dangerouslySetInnerHTML={{
          __html: sanitizeHtml(msg.message, {
            allowedTags: ["img"],
            allowedAttributes: {
              img: ["src", "title", "class"],
            },
          }),
        }}
      ></span>
    </div>
  );
}

function fixColor(color) {
  switch (color) {
    case "#0000ff":
      return "#8b58ff";
    case "#8A2BE2":
      return "#8b58ff";
    case "#000000":
      return "#7A7A7A";
    case "#3A2B2B":
      return "#877587";
    default:
      return color;
  }
}

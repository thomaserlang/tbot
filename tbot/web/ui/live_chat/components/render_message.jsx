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
  switch (color.toUpperCase()) {
    case "#0000FF":
      return "#8b58FF";
    case "#8A2BE2":
      return "#8B58FF";
    case "#000000":
      return "#7A7A7A";
    case "#3A2B2B":
      return "#877587";
    case "#893939":
      return "#B7625F";
    case "#4D4C4D":
      return "#7D7E7F";
    case "#191D59":
      return "#837AC3";
    case "#0E3820":
      return "#5B8969";
    case "#161917":
      return "#7A7A7A";
    case "#5900FF":
      return "#9F4EFF";
    case "#2626D3":
      return "#8061FF";
    default:
      return color;
  }
}

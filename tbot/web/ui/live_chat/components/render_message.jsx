import React from "react";
import sanitizeHtml from "sanitize-html";
import { providerShort } from "./provider_short";
import "./chat.scss";

export function RenderMessage({ msg }) {
  return (
    <div className="message">
      <div className="time">
        {new Date(msg.created_at).toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
          hour12: false,
        })}
      </div>

      {providerShort(msg.provider)}

      <div
        className="badges"
        dangerouslySetInnerHTML={{
          __html: sanitizeHtml(msg.badgesHTML, {
            allowedTags: ["img"],
            allowedAttributes: {
              img: ["src", "title", "class"],
            },
          }),
        }}
      ></div>

      <div>
        <span className="username" style={{ color: msg.user_color }}>
          {msg.user}
        </span>
        :
      </div>

      <div
        className="text"
        dangerouslySetInnerHTML={{
          __html: sanitizeHtml(msg.message, {
            allowedTags: ["img"],
            allowedAttributes: {
              img: ["src", "title", "class"],
            },
          }),
        }}
      ></div>
    </div>
  );
}

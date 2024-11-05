import { providerShort } from "./provider_short";
import sanitizeHtml from "sanitize-html";

export function RenderNotice({ msg }) {
  return (
    <div className="notice">
      {providerShort(msg.provider)}
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

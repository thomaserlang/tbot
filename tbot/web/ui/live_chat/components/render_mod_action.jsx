import { providerShort } from "./provider_short";

export function RenderModAction({ msg }) {
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
      <span className="time">{msg.message}</span>
    </div>
  );
}

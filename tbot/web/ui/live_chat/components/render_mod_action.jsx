import { providerShort } from "./provider_short";

export function RenderModAction({ msg }) {
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
      <div className="time">{msg.message}</div>
    </div>
  );
}

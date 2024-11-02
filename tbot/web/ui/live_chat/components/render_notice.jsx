import { providerShort } from "./provider_short";

export function RenderNotice({ msg }) {
  return (
    <div className="notice">
      {providerShort(msg.provider)}
      <span className="text">{msg.message}</span>
    </div>
  );
}

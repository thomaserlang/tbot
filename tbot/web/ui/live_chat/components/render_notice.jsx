export function RenderNotice({ msg }) {
  return (
    <div className="notice">
      <div className="text">{msg.message}</div>
    </div>
  );
}

export function RenderNotice({ msg }) {
  return (
    <div className="notice">
      <span className="text">{msg.message}</span>
    </div>
  );
}

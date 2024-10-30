import { Chat } from "./components/chat";

export default function Component(props) {
  const channelId = props.match.params.channelId;
  return <Chat channelId={channelId} />;
}

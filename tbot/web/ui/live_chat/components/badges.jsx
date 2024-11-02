import { useQuery } from "react-query";
import api from "tbot/twitch/api";

export function Badges({ channelId, badges }) {
  const { data, isLoading } = useQuery(
    ["badges", channelId],
    async () => {
      const data = await api.get(`/api/twitch/channels/${channelId}/badges`);
      return [...data.data.global_badges, ...data.data.channel_badges];
    },
    {
      staleTime: 1000 * 60 * 60,
      cacheTime: 1000 * 60 * 60,
    }
  );
  if (isLoading || !badges) {
    return <></>;
  }
  const items = badges.split(",");
  const parsedBadges = items.map((item) => {
    const [set_id, id] = item.split("/");
    return { set_id, id };
  });
  return (
    <>
      {parsedBadges.map((badge) => {
        const b = findBadge(data, badge.set_id, badge.id);
        if (b)
          return (
            <img
              key={[badge.set_id, badge.id]}
              title={b.title}
              className="chat-badge"
              src={b.image_url_1x}
            ></img>
          );
      })}
    </>
  );
}

function findBadge(badges, set_id, id) {
  for (const badge of badges) {
    if (badge.set_id === set_id) {
      for (const version of badge.versions) {
        if (version.id === id) {
          return version;
        }
      }
    }
  }
}

import { useState, useEffect, useCallback } from "react";
import { EmoteFetcher, EmoteParser } from "@mkody/twitch-emoticons";

const fetcher = new EmoteFetcher();
const parser = new EmoteParser(fetcher, {
  template: '<img class="emote" alt="{name}" src="{link}">',
  match: /(\w+)+?/g,
});

export function useParseEmotes({ channelId }) {
  const [loading, setLoading] = useState(true);
  const [loadEmotes, setLoadEmotes] = useState(1);

  useEffect(() => {
    Promise.all([
      fetcher.fetchBTTVEmotes(),
      fetcher.fetchBTTVEmotes(channelId),
      fetcher.fetchSevenTVEmotes(),
      fetcher.fetchSevenTVEmotes(channelId),
      fetcher.fetchFFZEmotes(),
      fetcher.fetchFFZEmotes(channelId),
    ])
      .then(() => {
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error loading emotes...");
        console.error(err);
        setLoadEmotes((prev) => prev + 1);
      });
  }, [loadEmotes]);

  const parseEmoteMessage = useCallback((message) => {
    if (!loading) {
      return message;
    }
    return parser.parse(message);
  }, []);

  return { parseEmoteMessage, loading };
}

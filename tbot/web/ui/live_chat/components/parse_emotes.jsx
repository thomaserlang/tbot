import { useState, useEffect, useCallback } from "react";
import {
  EmoteFetcher,
  EmoteParser,
  TwitchEmote,
} from "@mkody/twitch-emoticons";

import api from "tbot/twitch/api";

const fetcher = new EmoteFetcher();
const parser = new EmoteParser(fetcher, {
  template: '<img class="emote" alt="{name}" src="{link}">',
  match: /(\w+)+?/g,
});

export function useParseEmotes({ channelId }) {
  const [loading, setLoading] = useState(true);
  const [loadEmotes, setLoadEmotes] = useState(1);

  useEffect(() => {
    if (loadEmotes > 5) return;
    Promise.all([
      api.get(`/api/twitch/channels/${channelId}/emotes`),
      fetcher.fetchBTTVEmotes(),
      fetcher.fetchBTTVEmotes(channelId),
      fetcher.fetchSevenTVEmotes(),
      fetcher.fetchSevenTVEmotes(channelId),
      fetcher.fetchFFZEmotes(),
      fetcher.fetchFFZEmotes(channelId),
    ])
      .then((data) => {
        const emotes = [];
        for (const emote of data[0].data.global_emotes) {
          emote.formats = emote.format;
          emote.code = emote.name;
          emotes.push(
            new TwitchEmote(fetcher.channels.get(channelId), emote.id, emote)
          );
        }
        for (const emote of data[0].data.channel_emotes) {
          emote.formats = emote.format;
          emote.code = emote.name;
          emotes.push(
            new TwitchEmote(fetcher.channels.get(channelId), emote.id, emote)
          );
        }
        fetcher.fromObject(emotes.map((emote) => emote.toObject()));
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error loading emotes...");
        console.error(err);
        setTimeout(() => setLoadEmotes((prev) => prev + 1), 500);
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

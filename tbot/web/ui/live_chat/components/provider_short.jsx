export function providerShort(provider) {
  switch (provider) {
    case "twitch":
      return (
        <span className="provider twitch" title="Twitch">
          T
        </span>
      );
    case "youtube":
      return (
        <span className="provider youtube" title="YouTube">
          Y
        </span>
      );
  }
}

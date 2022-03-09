---
id: lol
title: League of Legends
---

Example usage:

`@{user}, Rank: {lol.tier} {lol.rank} (LP: {lol.lp}) {lol.summoner "ErlePerle" "euw1"}`

Response: `@user, Rank: IRON 4 (LP: 0)`

## lol.summoner

Set the name and region of the user to lookup. Is required.

`{lol.summoner "<name>" "<region>"}`

Valid regions: euw1, ru, kr, br1, oc1, jp1, na1, eun1, tr1, la1, la2

Returns an empty string.

## lol.tier

Current tier.

`{lol.tier}`

Example response: `PLATINUM`

## lol.rank

Current rank in their tier.

`{lol.rank}`

Example response: `II`

## lol.lp

Current League Points.

`{lol.lp}`

Example response: `74`

## lol.wins

Number of wins.

`{lol.wins}`

Example response: `20`

## lol.losses

Number of losses.

`{lol.losses}`

Example response: `10`

## lol.live_wins
The number of wins since the stream went live.

`{lol.live_wins}`

Example response: `1`

## lol.live_losses
The number of losses since the stream went live.

`{lol.live_losses}`

Example response: `5`

## Riot notice

BotAsHell isn’t endorsed by Riot Games and doesn’t reflect the views or opinions of Riot Games
or anyone officially involved in producing or managing League of Legends. League of Legends and Riot Games are
trademarks or registered trademarks of Riot Games, Inc. League of Legends © Riot Games, Inc.
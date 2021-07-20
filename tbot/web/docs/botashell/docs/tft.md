---
id: tft
title: Teamfight Tactics
---

Example usage:

`@{user}, Rank: {tft.tier} {tft.rank} (LP: {tft.lp}) {tft.summoner "ErlePerle" "euw1"}`

Response: `@user, Platinum III (LP: 93)`

## tft.summoner

Set the name and region of the user to lookup. Is required.

`{tft.summoner "<name>" "<region>"}`

Valid regions: euw1, ru, kr, br1, oc1, jp1, na1, eun1, tr1, la1, la2

Returns an empty string.

## tft.tier

Current tier.

`{tft.tier}`

Example response: `Platinum`

## tft.rank

Current rank in their tier.

`{tft.rank}`

Example response: `II`

## tft.lp

Current League Points.

`{tft.lp}`

Example response: `74`

## tft.wins

Number of wins.

`{tft.wins}`

Example response: `20`

## tft.losses

Number of losses.

`{tft.losses}`

Example response: `10`


## Riot notice

BotAsHell isn’t endorsed by Riot Games and doesn’t reflect the views or opinions of Riot Games
or anyone officially involved in producing or managing League of Legends. League of Legends and Riot Games are
trademarks or registered trademarks of Riot Games, Inc. League of Legends © Riot Games, Inc.
---
id: lol
title: League of Legends
---

Example usage:

`@{user}, Rank: {lol.tier} {lol.rank} (LP: {lol.lp}) {lol.summoner "ErlePerle" "euw1"}`


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
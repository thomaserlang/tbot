---
id: faceit
title: Faceit
---

Example usage:

`@{user}, Faceit level: {faceit.level} ({faceit.elo} elo) - {faceit.next_level_points} elo needed for next level {faceit.username ErlePerle}`


## faceit.username

Set the name of the faceit user to lookup

`{faceit.username ErlePerle}`

Returns an empty string.

## faceit.elo

The user's current elo.

`{faceit.elo}`

Example response: `1024`

## faceit.level

The user's current level.

`{faceit.level}`

Example response: `6`

## faceit.next_level_points

The amount of points needed for the next level.

`{faceit.next_level_points}`

Example response: `106`

## faceit.next_level

The name of the next level.

`{faceit.next_level}`

Example response: `7`

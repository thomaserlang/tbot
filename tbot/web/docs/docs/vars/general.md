---
id: general
title: General
---

## User

`{user}`

Defaults to the user that triggered the command or the user mentioned in the first argument of the command `!test ErlePerle`.

## Sender

`{sender}`

Name of the user that triggered the command.

## Channel

`{channel}`

Name of the current channel.

## Followers

`{followers}`

Current number of channel followers

## Views

`{views}`

Current number of channel views

## Countdown

Use the [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format. 

    `{countdown 2020-10-27T12:00:00+02}`

Example response: `1 month, 1 day and 19 hours`

## Random number

    `{randint}`
    `{randint 10}`
    `{randint 100 200}`

Example response: 113
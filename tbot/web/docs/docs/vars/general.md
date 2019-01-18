---
id: general
title: General
---

## Uptime

`{uptime}`

The time since the stream has been started.

Example response: `3 hours 18 mins`

**OBS:**  
There can be a delay of 1-3 minutes for it to start responding.  
If the stream shutdowns and resumes within 1 hour the counter resumes.  
So you will not lose your uptime in case of a crash. 

## Sender

`{sender}`

Name of the user that triggered the command.

## User

`{user}`

Defaults to the user that triggered the command or the user mentioned in the first argument of the command `!test ErlePerle`.

## Channel

`{channel}`

Name of the current channel.

## Alias

`{alias cmd}`

Trigger a command, replace `cmd` with the name of your command without a `!`.  
You can trigger multiple commands by separating them by a space, example: `{alias twitter instagram}`

## Command manager

`{cmd_manager}`

Manage your commands from the chat.

Example: `!cmd add/edit/delete/get [cmd] <response>`

## Accountage

`{accountage}`

Example response: `5 years, 8 months, 13 days and 2 hours`

`{accountage_date}`

Example response: `2013-06-03`

`{accountage_datetime}`

Example response: `2013-06-03 19:12:02 UTC`


## Followage

`{followage}`

Example response: `5 years, 8 months, 13 days and 2 hours`

`{followage_date}`

Example response: `2013-06-03`

`{followage_datetime}`

Example response: `2013-06-03 19:12:02 UTC`
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

Defaults to the user that triggered the command or the user mentioned in the first argument of the commend `!test ErlePerle`.

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
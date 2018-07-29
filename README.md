# tbot
Bot for Twitch chat and Discord.

## Twitch chat
Keeps track of the viewer's watchtime and the amount of streams in a row the viewer has shown up for.
For the chatstats `Logitch` must be running.

Support for extra long offline detection in case your stream shutsdown for just a minute the stream uptime will not be reset.
Default you have 1 hour to resume the stream. The uptime only counts the online time.

### Commands

| Command | Alias | Example | 
| - | - | - |
| !streamuptime | !sup | This stream has been live for 3 hours 23 mins |
| !streamwatchtime | !swt | ErlePerle has been here for 2 hours 5 mins this stream (100%) |
| !streamsinarow | !siar | ErlePerle has been here for 2 streams in a row (Peak: 5, 2018-06-28) and a total of 7 streams |
| !totalchatstats | | Channel chat stats: This stream: 1215 messages / 6372 words |
| !chatstats | | Wossadinho: This stream: 398 messages / 1359 words - This month: 3919 messages / 12143 words |
| !chatstatslastmonth | | Wossadinho: Last month: 15401 messages / 56488 words | 
| !spotifysong | !ssong | Playing: Shots by Imagine Dragons (0:18/3:52) | 
| !spotifyprevsong | !sprevsong | Previous song: Stressed Out by Twenty One Pilots |
| !spotifyplaylist | !splaylist | Current playlist: https://open.spotify.com/user/... | 

## Discord
Gives roles to users for their sub streak and sub tier for the connected Twitch channel. Syncs once an hour.

| Command | Info | 
| - | - |
| !twitchsync | Force the bot to sync instead of waiting for 1 hour. |

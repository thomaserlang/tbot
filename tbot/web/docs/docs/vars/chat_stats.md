---
id: chat_stats
title: Chat stats
---

If the first argument of the command is another user, data from that user will be retrieved instead.

## Stream

### Total messages
Total number of messages written during the current stream.

`{chat_stats.stream_msgs}` e.g. `300 messages`

`{chat_stats.stream_msgs_num}` e.g. `300`


### Total words

Total number of words written during the current stream.

`{chat_stats.stream_words}` e.g. `520 words`

`{chat_stats.stream_words_num}` e.g. `520`


## User

### Total messages

A user's total number of messages written in the chat.

`{user.chat_stats.total_msgs}` e.g `700 messages`

`{user.chat_stats.total_msgs_num}` e.g `700`


### Stream messages

The number of messages the user has written in the current stream.

`{user.chat_stats.stream_msgs}` e.g. `10 messages`

`{user.chat_stats.stream_msgs_num}` e.g. `10`


### Stream words

The number of words the user has written in the current stream.

`{user.chat_stats.stream_words}` e.g. `20 words`

`{user.chat_stats.stream_words_num}` e.g. `20`


### Month messages

The number of messages the user has written for the current month.

`{user.chat_stats.month_msgs}` e.g. `321 messages`

`{user.chat_stats.month_msgs_num}` e.g. `321`

### Month words

The number of words the user has written for the current month.

`{user.chat_stats.month_words}` e.g. `600 words`

`{user.chat_stats.month_words_num}` e.g. `600`

### Last month messages

The number of messages the user wrote last month.

`{user.chat_stats.last_month_msgs}` e.g. `825 messages`

`{user.chat_stats.last_month_msgs_num}` e.g. `825`

### Last month words

The number of words the user wrote last month.

`{user.chat_stats.last_month_words}` e.g. `1100 words`

`{user.chat_stats.last_month_words_num}` e.g. `1100`

### Bans

How many times a user has been banned in the chat.

`{user.chat_stats.bans}` e.g. `1 time`

`{user.chat_stats.bans_num}` e.g. `1`

### Timeouts

How many times a user has been timed out in the chat.

`{user.chat_stats.timeouts}` e.g. `2 times`

`{user.chat_stats.timeouts_num}` e.g. `2`

### Bans

How many times a user has been purged in the chat. A purge is a timeout of 1 second.

`{user.chat_stats.purges}` e.g. `5 times`

`{user.chat_stats.purges_num}` e.g. `5`

### Deletes

How many times a user's message has been deleted. 
Bans, timeouts and purges are are not counted here.
Only when a mod specifically deletes a message in chat.

`{user.chat_stats.deletes}` e.g. `13 times`

`{user.chat_stats.deletes_num}` e.g. `13`
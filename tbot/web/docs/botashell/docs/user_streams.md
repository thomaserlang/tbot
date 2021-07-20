---
id: user_streams
title: User streams
---

If the first argument of the command is another user, data from that user will be retrieved instead.

## Stream watchtime 

`{user.stream_watchtime}`

The amount of time the user has watched the current stream.

Example response: `2 hours 42 mins`

## Stream watchtime percent

`{user.stream_watchtime_percent}`

How many percent the user has watched of the current stream. 

Example response: `43%`

## Streams in a row
    
`{user.streams_row}`

The number of streams the user has been there for in a row.

Example response: `9`

## Streams in a row peak

`{user.streams_row_peak}`

The user's peak number of streams in a row.

Example response: `12`

## Streams in a row peak date

`{user.streams_row_peak_date}`

The date of when the peak was set.

Example response: `2019-01-01`

## Streams in a row text

`{user.streams_row_text}`

A pregenerated message for a user's streams in a row.

Example responses:

If the current streams in a row is lower than the peak:  
`ErlePerle has been here for 27 streams in a row (Peak: 64, 2018-02-08) and a total of 179 streams`

If the current number of streams in a row is higher or equal to the peak:  
`ErlePerle has been here for 65 streams in a row and a total of 217 streams`

## Total streams

`{user.streams_total}`

The total number of streams the user has been there for.

Example response: `20`
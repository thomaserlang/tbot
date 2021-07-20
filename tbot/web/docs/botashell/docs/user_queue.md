---
id: user_queue
title: User queue
---

## User

### Join

`{user_queue.join}`

Adds the sender to the queue and returns their display name.

Example response: `ErlePerle`

`{user_queue.join_pos}`

Returnes the added position in the queue

Example response: `7`

### Unjoin

`{user_queue.unjoin}`

Removes the sender from the queue. Returns their display name.

Example response: `ErlePerle`

`{user_queue.unjoin_count}`

Returns the number of users left in the queue after removing the user.

Example response: `7`

`{user_queue.unjoin_count_text}`

Example response: `7 users`

### Count

`{user_queue.count}`

Returns the number of users in the queue.

Example response: `7`

`{user_queue.count_text}`

Example response: `7 users`

### Position

`{user_queue.pos}`

Returns the position of the sender in the queue.

Example response: `7`

### Top 5

`{user_queue.top_5}`

Example response: `1. ErlePerle - .. 5. erle4000`

## For admins

### Next

Returns the next user in the queue and removes them at the same time.

`{user_queue_admin.next}`

Example response: `ErlePerle`

`{user_queue_admin.next_count}`

Returns the number of users left after the next person has been removed.

Example response: `12`

`{user_queue_admin.next_count_text}`

Example response: `12 users`

### Remove

Returns the next user in the queue and removes them at the same time.
The 1st argument of the command must be the user to add. E.g. `!add erleperle`

`{user_queue_admin.next}`

Example response: `ErlePerle`

`{user_queue_admin.remove_count}`

Returns the number of users left after the next person has been removed.

Example response: `12`

`{user_queue_admin.remove_count_text}`

Example response: `12 users`

### Promote

Promotes a user to the top of the queue. They do not have to be in the queue already.

`{user_queue_admin.promote}`

Example response: `ErlePerle`

### Add

Add a user to the queue. The 1st argument of the command must be the user to add. E.g. `!add erleperle`

`{user_queue_admin.add}`

Example response: `ErlePerle`

`{user_queue_admin.add_pos}`

The position the user was added as.

Example response: `15`

### Clear

`{user_queue_admin.add}`

Clears the queue. Just returns an empty string.
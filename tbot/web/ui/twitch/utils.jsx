
export function isAuthed() {
	return tbot.twitch_user !== null;
}

export function requireAuth() {
	if (!isAuthed()) {
        let next = encodeURIComponent(
            location.pathname + location.search
        )
        location.href = '/twitch/login?next='+next;
		throw 'Not authenticated!';
	}
}

export function userLevelName(level) {
    switch (level) {
        case 0:
            return 'Everyone'
            break
        case 1:
            return 'Sub'
            break
        case 2:
            return 'VIP'
            break
        case 7:
            return 'Mod'
            break
        case 8:
            return 'Admin'
            break
        case 9:
            return 'Broadcaster'
            break
        default:
            return 'Unknown user level'
    }
}

export function enabledWhenName(level) {
    switch (level) {
        case 0:
            return 'Always'
            break
        case 1:
            return 'Online'
            break
        case 2:
            return 'Offline'
            break
        default:
            return 'Unknown enabled when level'
    }
}
"""
Added min_amount to twitch_chat_alerts
"""

from yoyo import step

__depends__ = {'20190505_01_HmBmL-twitch-discord-live-notification'}

steps = [
    step("ALTER TABLE twitch_chat_alerts ADD COLUMN min_amount INT NULL AFTER message;")
]

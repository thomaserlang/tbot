"""
twitch scope length
"""

from yoyo import step

__depends__ = {'20220625_01_wQvKe-spotify-token-length'}

steps = [
    step("ALTER TABLE twitch_channels CHANGE COLUMN twitch_scope twitch_scope VARCHAR(1000) NULL DEFAULT NULL;")
]

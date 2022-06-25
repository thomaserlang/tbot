"""
spotify token length
"""

from yoyo import step

__depends__ = {'20210918_01_DxCKw-twitch-widget-keys'}

steps = [
    step('''
        ALTER TABLE twitch_spotify 
        CHANGE COLUMN token token VARCHAR(500) NOT NULL ,
        CHANGE COLUMN refresh_token refresh_token VARCHAR(500) NOT NULL ;
    ''')
]

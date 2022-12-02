"""
twitch_stream_watchtime index
"""

from yoyo import step

__depends__ = {'20221128_01_rQWlg-twitch-scope-length'}

steps = [
    step('''
        ALTER TABLE twitch_stream_watchtime 
            DROP PRIMARY KEY,
            ADD PRIMARY KEY (channel_id, user_id, stream_id);
    ''')
]

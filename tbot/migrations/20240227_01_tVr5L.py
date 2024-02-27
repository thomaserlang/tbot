"""

"""

from yoyo import step

__depends__ = {'20240226_03_eKhC6'}

steps = [
    step('''
        ALTER TABLE `twitch_sub_log`
            CHANGE `plan_name` `message` varchar(2000) NULL DEFAULT NULL,
            ADD COLUMN `user` VARCHAR(200) COMMENT '',
            ADD COLUMN `gifter_user` VARCHAR(200) COMMENT '';     
    ''')
]
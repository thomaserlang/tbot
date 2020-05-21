"""
twitch quotes
"""

from yoyo import step

__depends__ = {'20191025_01_SaqGl-support-filter-groups'}

steps = [
    step('''
        CREATE TABLE IF NOT EXISTS `twitch_quotes` (
          `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
          `channel_id` VARCHAR(36) NULL DEFAULT NULL,
          `created_by_user_id` VARCHAR(36) NULL DEFAULT NULL,
          `created_by_user` VARCHAR(25) NULL DEFAULT NULL,
          `created_at` DATETIME NULL DEFAULT NULL,
          `updated_at` DATETIME NULL DEFAULT NULL,
          `number` INT(10) UNSIGNED NULL DEFAULT NULL,
          `message` VARCHAR(400) NULL DEFAULT NULL,
          `enabled` INT(1) UNSIGNED NULL DEFAULT NULL,
          PRIMARY KEY (`id`),
          INDEX `ix_twitch_quotes_channel_id_number` (`channel_id` ASC, `number` ASC))
        ENGINE = InnoDB
        DEFAULT CHARACTER SET = utf8mb4;
    '''),

    step('''
      DROP TRIGGER IF EXISTS `twitch_quotes_BEFORE_INSERT`;
    '''),

    step('''
        CREATE `twitch_quotes_BEFORE_INSERT` BEFORE INSERT ON `twitch_quotes` FOR EACH ROW
        BEGIN
            declare n int;
            set n = (select ifnull(max(number), 0)+1 from twitch_quotes where channel_id=new.channel_id);
            set new.number = n;
        END
    '''),
]

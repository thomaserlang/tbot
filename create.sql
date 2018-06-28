CREATE SCHEMA IF NOT EXISTS `tbot` DEFAULT CHARACTER SET utf8mb4 ;
USE `tbot` ;

CREATE TABLE IF NOT EXISTS `tbot`.`stream_watchtime` (
  `channel_id` INT(11) UNSIGNED NOT NULL,
  `stream_id` VARCHAR(75) NOT NULL,
  `user_id` INT(11) UNSIGNED NOT NULL,
  `user` VARCHAR(45) NULL,
  `time` INT NULL,
  PRIMARY KEY (`stream_id`, `user_id`, `channel_id`))
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `tbot`.`channel_cache` (
  `channel_id` INT(11) UNSIGNED NOT NULL,
  `data` TEXT NULL,
  PRIMARY KEY (`channel_id`))
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `tbot`.`commands` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `channel` VARCHAR(50) NOT NULL,
  `cmd` VARCHAR(50) NOT NULL,
  `text` VARCHAR(500) NOT NULL,
  `user_level` ENUM('everyone', 'mod', 'sub') NOT NULL DEFAULT 'everyone',
  `global_cooldown` INT UNSIGNED NOT NULL DEFAULT 0,
  `user_cooldown` INT UNSIGNED NOT NULL DEFAULT 5,
  `enabled_when` ENUM('online', 'offline', 'alltime') NOT NULL DEFAULT 'alltime',
  PRIMARY KEY (`id`),
  UNIQUE INDEX `ix_commands_channel_cmd` (`channel` ASC, `cmd` ASC))
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `tbot`.`command_aliases` (
  `channel` VARCHAR(50) NOT NULL,
  `alias` VARCHAR(45) NOT NULL,
  `command_id` INT UNSIGNED NULL,
  PRIMARY KEY (`channel`, `alias`),
  INDEX `fk_command_aliases_command_id_idx` (`command_id` ASC),
  CONSTRAINT `fk_command_aliases_command_id`
    FOREIGN KEY (`command_id`)
    REFERENCES `tbot`.`commands` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `tbot`.`user_stats` (
  `channel_id` INT(11) UNSIGNED NOT NULL,
  `user_id` INT(11) UNSIGNED NOT NULL,
  `user` VARCHAR(45) NULL,
  `streams` INT UNSIGNED NOT NULL DEFAULT 0,
  `streams_row` INT UNSIGNED NOT NULL DEFAULT 0,
  `streams_row_peak` INT UNSIGNED NOT NULL DEFAULT 0,
  `streams_row_peak_date` DATE NULL,
  `last_viewed_stream_id` VARCHAR(75) NULL,
  `last_viewed_stream_date` DATE NULL,
  PRIMARY KEY (`user_id`, `channel_id`))
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `tbot`.`streams` (
  `stream_id` VARCHAR(75) NOT NULL,
  `channel_id` INT(11) UNSIGNED NOT NULL,
  `started_at` DATETIME NULL,
  `ended_at` DATETIME NULL,
  PRIMARY KEY (`stream_id`))
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `tbot`.`channels` (
  `channel_id` INT(11) UNSIGNED NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `active` ENUM('Y', 'N') NULL DEFAULT 'Y',
  `created_at` DATETIME NOT NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`channel_id`))
ENGINE = InnoDB;

USE `tbot`;

DELIMITER $$
USE `tbot`$$
CREATE
TRIGGER `tbot`.`stream_watchtime_AFTER_INSERT`
AFTER INSERT ON `tbot`.`stream_watchtime`
FOR EACH ROW
BEGIN
	INSERT INTO user_stats 
		(channel_id, user_id, user, streams, streams_row, streams_row_peak, 
        streams_row_peak_date, last_viewed_stream_id, 
        last_viewed_stream_date)
	VALUES
		(new.channel_id, new.user_id, new.user, 1, 1, 1, date(now()), new.stream_id, date(now()))
	ON DUPLICATE KEY UPDATE 
		user=new.user,
		streams=streams+1,
        streams_row=streams_row+1,
        last_viewed_stream_id=new.stream_id,
        last_viewed_stream_date=date(now());
END$$

USE `tbot`$$
CREATE
TRIGGER `tbot`.`user_stats_BEFORE_UPDATE`
BEFORE UPDATE ON `tbot`.`user_stats`
FOR EACH ROW
BEGIN
	if new.streams_row > new.streams_row_peak then
		set new.streams_row_peak = new.streams_row;
        set new.streams_row_peak_date = date(now());
    end if;
END$$


DELIMITER ;
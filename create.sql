
CREATE SCHEMA IF NOT EXISTS `tbot` DEFAULT CHARACTER SET utf8mb4 ;
USE `tbot` ;

CREATE TABLE IF NOT EXISTS `tbot`.`stream_watchtime` (
  `channel` VARCHAR(45) NOT NULL,
  `stream_id` VARCHAR(75) NOT NULL,
  `user` VARCHAR(45) NOT NULL,
  `time` INT NULL,
  PRIMARY KEY (`channel`, `user`, `stream_id`))
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `tbot`.`channel_cache` (
  `channel` VARCHAR(50) NOT NULL,
  `data` TEXT NULL,
  PRIMARY KEY (`channel`))
ENGINE = InnoDB;

CREATE SCHEMA `tbot` DEFAULT CHARACTER SET utf8mb4 ;

CREATE TABLE IF NOT EXISTS `tbot`.`current_stream_watchtime` (
  `channel` VARCHAR(45) NOT NULL,
  `user` VARCHAR(45) NOT NULL,
  `time` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`channel`, `user`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;
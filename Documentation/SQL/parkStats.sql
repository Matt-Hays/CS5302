DROP TABLE IF EXISTS `parkStats`;
SET character_set_client = utf8mb4;

CREATE TABLE `parkStats` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `parkkey` varchar(255) NOT NULL,
  `yearID` smallint(6) NOT NULL,
  `H` smallint(6) DEFAULT NULL,
  `R` smallint(6) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID` (`parkkey`,`yearID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

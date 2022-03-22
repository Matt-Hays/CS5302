DROP TABLE IF EXISTS `PitchingAgainst`;

CREATE TABLE `PitchingAgainst` (
`ID` int(11) NOT NULL AUTO_INCREMENT,
`playerID` varchar(9) NOT NULL,
`yearID` smallint(6) NOT NULL,
`stint` smallint(6) NOT NULL,
`teamID` char(3) DEFAULT NULL,
`lgID` char(2) DEFAULT NULL,
`SO` smallint(6) DEFAULT NULL,
`SB` smallint(6) DEFAULT NULL,
`CS` smallint(6) DEFAULT NULL,
`PO` smallint(6) DEFAULT NULL,
`PB` smallint(6) DEFAULT NULL,
`W` smallint(6) DEFAULT NULL,
`IW` smallint(6) DEFAULT NULL,
`H` smallint(6) DEFAULT NULL,
`2B` smallint(6) DEFAULT NULL,
`3B` smallint(6) DEFAULT NULL,
`HR` smallint(6) DEFAULT NULL,
`RBI` smallint(6) DEFAULT NULL,
PRIMARY KEY (`ID`),
UNIQUE KEY `playerID` (`playerID`,`yearID`,`stint`),
KEY `lgID` (`lgID`),
CONSTRAINT `pa_lgfk` FOREIGN KEY (`lgID`) REFERENCES `leagues` (`lgID`),
CONSTRAINT `pa_playerfk` FOREIGN KEY (`playerID`) REFERENCES `people` (`playerID`)
)  ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



-- Using template from analysis.sql:

DROP TABLE IF EXISTS `PitchingAgainst`;
SET character_set_client = utf8mb4;
CREATE TABLE `PitchingAgainst` (
  `against_ID` int(11) NOT NULL AUTO_INCREMENT,
  `playerID` varchar(9) NOT NULL,
  `yearID` smallint(6) NOT NULL,
  `stint` smallint(6) DEFAULT NULL,
  `teamID` char(3) DEFAULT NULL, 
  `team_ID` int(11) DEFAULT NULL,
  `lgID`char(2) DEFAULT NULL,
  `G` smallint(6) DEFAULT NULL, 
  `G_batting` smallint(6) DEFAULT NULL, 
  `AB` smallint(6) DEFAULT NULL,
  `R` smallint(6) DEFAULT NULL,
  `H` smallint(6) DEFAULT NULL,
  `2B` smallint(6) DEFAULT NULL,
  `3B` smallint(6) DEFAULT NULL,
  `HR` smallint(6) DEFAULT NULL,
  `RBI` smallint(6) DEFAULT NULL,
  `SB` smallint(6) DEFAULT NULL,
  `CS` smallint(6) DEFAULT NULL,
  `BB` smallint(6) DEFAULT NULL,
  `SO` smallint(6) DEFAULT NULL,
  `IBB` smallint(6) DEFAULT NULL,
  `HBP` smallint(6) DEFAULT NULL,
  `SH` smallint(6) DEFAULT NULL,
  `SF` smallint(6) DEFAULT NULL,
  `GIDP` smallint(6) DEFAULT NULL,
  PRIMARY KEY (`against_ID`),
  UNIQUE KEY `against_ID` (`playerID`,`yearID`),
  CONSTRAINT `against_peoplefk` FOREIGN KEY (`playerID`) REFERENCES `people` (`playerID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO PitchingAnalytics(playerID, yearID, stint, teamID, lgID, G, R, H, HR, BB, SO, IBB, HBP, SH, SF, GIDP) 
SELECT playerID, yearID, stint, teamID, lgID, G, R, H, HR, BB, SO, IBB, HBP, SH, SF, GIDP 
FROM pitching GROUP BY playerID, yearID;

-- not sure what to do about G_batting and team_ID yet as these are not documented on Lahman's website
-- need to pull AB, 2B, 3B, RBI, SB, and CS from the Retrosheet data

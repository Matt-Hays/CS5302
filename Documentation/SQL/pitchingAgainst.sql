-- Using template from analysis.sql:

--
-- Table structure for table `pitchingAgainst`
--

DROP TABLE IF EXISTS `PitchingAgainst`;
SET character_set_client = utf8mb4;
CREATE TABLE `PitchingAgainst` (
  `against_ID` int(11) NOT NULL AUTO_INCREMENT,
  `playerID` varchar(9) NOT NULL,
  `yearID` smallint(6) NOT NULL,
  `stint` smallint(6) DEFAULT NULL,
  `teamID` char(3) DEFAULT NULL,
  `lgID`char(2) DEFAULT NULL,
  `G` smallint(6) DEFAULT NULL,
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
  UNIQUE KEY `player_ID` (`playerID`,`yearID`,`stint`),
  CONSTRAINT `against_peoplefk` FOREIGN KEY (`playerID`) REFERENCES `people` (`playerID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert all rows and columns from the pitching table into the corresponding columns in the PitchingAgainst table
INSERT INTO PitchingAgainst(playerID, yearID, stint, teamID, lgID, G, R, H, HR, BB, SO, IBB, HBP, SH, SF, GIDP)
SELECT playerID, yearID, stint, teamID, lgID, G, R, H, HR, BB, SO, IBB, HBP, SH, SF, GIDP
FROM pitching GROUP BY playerID, yearID;

-- Using template from analysis.sql:

--
-- Table structure for table `pitchingAnalytics`
--

DROP TABLE IF EXISTS `PitchingAnalytics`;
SET character_set_client = utf8mb4;
CREATE TABLE `PitchingAnalytics` (
  `analytics_ID` int(11) NOT NULL AUTO_INCREMENT,
  `playerID` varchar(9) NOT NULL,
  `yearID` smallint(6) NOT NULL,
  `stint` smallint(6) DEFAULT NULL,
  `teamID` char(3) DEFAULT NULL,
  `team_ID` int(11) DEFAULT NULL,
  `lgID`char(2) DEFAULT NULL,
  `TB` smallint(6) DEFAULT NULL, -- total bases
  `TW` decimal(5,2) DEFAULT NULL, -- total walks
  `SS` decimal(5,2) DEFAULT NULL, -- sacrifices and steals
  `TOB` smallint(6) DEFAULT NULL, -- times on base
  `BA` decimal(5,2) DEFAULT NULL, -- bases advanced
  `PA` smallint(6) DEFAULT NULL, -- plate appearances
  `RC` decimal(5,1) DEFAULT NULL, -- runs created
  `PARC` decimal(4,3) DEFAULT NULL, -- park-adjusted runs created = RC/((teams.BPF+100)/200)
  `PARC27` decimal(4,3) DEFAULT NULL,-- park-adjusted runs created per 27 outs = (PARC*27)/(AB+SF+SH+CS+GIDP-H)
  `PARCA` decimal(4,3) DEFAULT NULL, -- park-adjusted runs against = ???
  PRIMARY KEY (`analytics_ID`),
  UNIQUE KEY `playerID` (`playerID`,`yearID`,`stint`),
  CONSTRAINT `analytics_peoplefk` FOREIGN KEY (`playerID`) REFERENCES `people` (`playerID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert all players from the pitchingAgainst table into the pitchingAnalytics table
INSERT INTO PitchingAnalytics(playerID, yearID, stint, teamID, team_ID, lgID)
SELECT playerID, yearID, stint, teamID, team_ID, lgID
FROM pitchingAgainst;

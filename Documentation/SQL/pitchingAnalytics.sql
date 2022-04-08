-- Using template from analysis.sql:

DROP TABLE IF EXISTS `PitchingAnalytics`;
SET character_set_client = utf8mb4;
CREATE TABLE `PitchingAnalytics` (
  `analytics_ID` int(11) NOT NULL AUTO_INCREMENT,
  `playerID` varchar(9) NOT NULL,
  `yearID` smallint(6) NOT NULL,
  `stint` smallint(6) DEFAULT NULL,
  `teamID` char(3) DEFAULT NULL,
  `lgID`char(2) DEFAULT NULL,
  `TB` smallint(6) DEFAULT NULL, -- total bases
  `TW` decimal(5,2) DEFAULT NULL, -- total walks
  `SS` decimal(5,2) DEFAULT NULL, -- sacrifices and steals
  `TOB` smallint(6) DEFAULT NULL, -- times on base
  `BA` decimal(5,2) DEFAULT NULL, -- bases advanced
  `PA` smallint(6) DEFAULT NULL, -- plate appearances
  `RC` decimal(5,1) DEFAULT NULL, -- runs created
  --`PARC` -- park-adjusted runs created = RC/((teams.BPF+100)/200)
  --`PARC27` -- park-adjusted runs created per 27 outs = (PARC*27)/(AB+SF+SH+CS+GIDP-H)
  --`PARCA` -- park-adjusted runs against = ???
  PRIMARY KEY (`against_ID`),
  UNIQUE KEY `against_ID` (`playerID`,`yearID`),
  CONSTRAINT `against_peoplefk` FOREIGN KEY (`playerID`) REFERENCES `people` (`playerID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

UPDATE PitchingAnalytics
SET TB = H+2*(2B)+3*(3B)+4*HR; -- 2B and 3B pulled from Retrosheet data, H and HR already in Pitching table

UPDATE PitchingAnalytics
SET TW = (BB+HBP-IBB)*0.26; -- all attributes already in Pitching table

UPDATE PitchingAnalytics
SET SS = (SH+SF+SB)*0.52; -- SB pulled from Retrosheet data, SH and SF already in Pitching table

UPDATE PitchingAnalytics
SET TOB = H+BB+HBP-CS+GIDP; -- CS pulled from Retrosheet data, H/BB/HBP/GIDP already in Pitching table

UPDATE PitchingAnalytics
SET BA = TB+TW+SS;

UPDATE PitchingAnalytics
SET PA = AB+BB+HBP+SF+SH; -- AB pulled from Retrosheet data, BB/HBP/SF/SH already in Pitching table

UPDATE PitchingAnalytics
SET RC = (TOB*BA)/PA;

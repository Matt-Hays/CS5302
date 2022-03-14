--
-- Table structure for table `analysis`
--

DROP TABLE IF EXISTS `analysis`;
SET character_set_client = utf8mb4;
CREATE TABLE `analysis` (
  `analysis_ID` int(11) NOT NULL AUTO_INCREMENT,
  `playerID` varchar(9) NOT NULL,
  `yearID` smallint(6) NOT NULL,
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
  `OBP` numeric(5,3) DEFAULT NULL,
  `TB` smallint(6) DEFAULT NULL,
  `RC` numeric(5,1) DEFAULT NULL,
  `RC27` numeric(5,2) DEFAULT NULL,
  PRIMARY KEY (`analysis_ID`),
  UNIQUE KEY `analysisID` (`playerID`,`yearID`),
  CONSTRAINT `analysis_peoplefk` FOREIGN KEY (`playerID`) REFERENCES `people` (`playerID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO analysis(playerid,yearid,g,ab,r,h,2b,3b,hr,rbi,sb,
cs,bb,so,ibb,hbp,sh,sf,gidp)
SELECT playerid,yearid, SUM(g),SUM(ab),SUM(r),SUM(h),SUM(2b),
SUM(3b),SUM(hr),SUM(rbi),SUM(sb), SUM(cs),SUM( bb),SUM(so),
SUM(ibb),SUM(hbp),SUM(sh),SUM(sf),SUM(gidp)
FROM batting GROUP BY playerid,yearid;

--
-- Table structure for table `BattingAnalytics`
--

DROP TABLE IF EXISTS `BattingAnalytics`;
SET character_set_client = utf8mb4;
CREATE TABLE `BattingAnalytics` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `playerID` varchar(9) NOT NULL,
  `yearID` smallint(6) NOT NULL,
  `G` smallint(6) DEFAULT NULL, -- games
  `AB` smallint(6) DEFAULT NULL, -- at bats
  `R` smallint(6) DEFAULT NULL, -- runs
  `H` smallint(6) DEFAULT NULL, -- singles
  `2B` smallint(6) DEFAULT NULL, -- doubles
  `3B` smallint(6) DEFAULT NULL, -- triples
  `HR` smallint(6) DEFAULT NULL, -- home runs
  `RBI` smallint(6) DEFAULT NULL, -- runs batted in
  `SB` smallint(6) DEFAULT NULL, -- stolen bases
  `CS` smallint(6) DEFAULT NULL, -- caught steeling
  `BB` smallint(6) DEFAULT NULL, -- base on balls
  `SO` smallint(6) DEFAULT NULL, -- strikeouts
  `IBB` smallint(6) DEFAULT NULL, -- intentional walks
  `HBP` smallint(6) DEFAULT NULL, -- hit by pitch
  `SH` smallint(6) DEFAULT NULL, -- scrifice hits
  `SF` smallint(6) DEFAULT NULL, -- sacrifice flies
  `GIDP` smallint(6) DEFAULT NULL, -- grounded into double plays
  `OBP` numeric(5,3) DEFAULT NULL, -- on base percentage
  `TB` smallint(6) DEFAULT NULL, -- total bases
  `RC` numeric(5,1) DEFAULT NULL, -- runs created
  `RC27` numeric(5,2) DEFAULT NULL, -- runs created per 27 outs
  PRIMARY KEY (`ID`),
  UNIQUE KEY `battingAnalyticsID` (`playerID`,`yearID`),
  CONSTRAINT `battingAnalytics_peoplefk` FOREIGN KEY (`playerID`) REFERENCES `people` (`playerID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO BattingAnalytics(playerid,yearid,g,ab,r,h,2b,3b,hr,rbi,sb,
cs,bb,so,ibb,hbp,sh,sf,gidp)
SELECT playerid,yearid, SUM(g),SUM(ab),SUM(r),SUM(h),SUM(2b),
SUM(3b),SUM(hr),SUM(rbi),SUM(sb), SUM(cs),SUM( bb),SUM(so),
SUM(ibb),SUM(hbp),SUM(sh),SUM(sf),SUM(gidp)
FROM batting GROUP BY playerid,yearid;

UPDATE BattingAnalytics ba SET
    TB = H+2B+2*3B+3*HR,
    OBP =
        CASE
            WHEN AB+BB+COALESCE(HBP,0)+COALESCE(SF,0) <> 0
                THEN (H+BB) / (AB+BB+COALESCE(HBP,0) + COALESCE(SF,0))
            ELSE 0
        END,
    RC = OBP * TB,
    RC27 =
        CASE
            WHEN (AB-H+COALESCE(SF,0)+COALESCE(SH,0)+COALESCE(GIDP,0)+COALESCE(CS,0)) <> 0
                THEN (RC * 27) / (AB-H+COALESCE(SF,0)+COALESCE(SH,0)+COALESCE(GIDP,0)+COALESCE(CS,0))
            ELSE 0
        END;

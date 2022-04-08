DELIMITER //

CREATE OR REPLACE TRIGGER updatePitchingAgainst
BEFORE UPDATE ON pitchingAgainst
FOR EACH ROW
BEGIN
IF (SELECT COUNT(*) FROM pitchingAgainst WHERE playerid = NEW.playerid) = 0 THEN
	INSERT INTO pitchingAgainst(playerid, yearid, stint, teamID, lgID, G, AB, R, H, 2B, 3B, HR, RBI, SB, CS, BB, SO, IBB, HBP, SH, SF, GIDP)
	VALUES(NULL, NULL, NULL, NULL, NULL, NULL, NEW.AB, NULL, NEW.H, NEW.2B, NEW.3B, NULL, NEW.RBI, NEW.SB, NEW.CS, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
END IF;
END;
//

DELIMITER ;

/*
-- Test for trigger
UPDATE PitchingAgainst SET H = 171, 2B = 31, 3B = 2, SB = 22, CS = 0, AB = 705, RBI = 66 WHERE playerID LIKE '%reedro01%' AND yearID = 1974 AND stint = 0;

-- Tests for successful update when playerID in Lahman db
SELECT playerID, yearID, stint, H, 2B, 3B, SB, CS, AB, RBI
FROM pitchingAgainst
WHERE playerID = 'reedro01' and yearID = 1974 AND stint = 0;

-- Tests for successful update when playerID not in Lahman db
SELECT playerID, yearID, stint, H, 2B, 3B, SB, CS, AB, RBI
FROM pitchingAgainst
WHERE playerID = NULL;
*/

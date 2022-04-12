-- Using template from trigger.sql
-- Every time PitchingAgainst is updated with Retrosheets data, update PitchingAnalytics with calculation results

DELIMITER //

CREATE OR REPLACE TRIGGER updatePitchingAnalytics
AFTER UPDATE ON PitchingAgainst
FOR EACH ROW
BEGIN
UPDATE PitchingAnalytics SET
    TB = NEW.H+2*(NEW.2B)+3*(NEW.3B)+4*NEW.HR,
    TW = (NEW.BB+NEW.HBP-NEW.IBB)*0.26,
    SS = (NEW.SH+NEW.SF+NEW.SB)*0.52,
    TOB = NEW.H+NEW.BB+NEW.HBP-NEW.CS+NEW.GIDP,
    BA = TB+TW+SS,
    PA = NEW.AB+NEW.BB+NEW.HBP+NEW.SF+NEW.SH,
    RC =
        CASE -- avoiding division by 0
				WHEN PA IS NOT NULL AND PA <> 0 THEN (TOB*BA)/PA
                WHEN PA IS NULL THEN NULL
		ELSE 0
		END,
    PARC = RC/(((SELECT BPF FROM teams WHERE yearID = NEW.yearID AND teamID = NEW.teamID)+100)/200),
    PARC27 = (PARC*27)/(NEW.AB+NEW.SF+NEW.SH+NEW.CS+NEW.GIDP-NEW.H),
    PARCA = RC/(((SELECT PPF FROM teams WHERE yearID = NEW.yearID AND teamID = NEW.teamID)+100)/200)
WHERE playerID = NEW.playerID AND yearID = NEW.yearID AND stint = NEW.stint;
END;
//

DELIMITER ;

/*
-- Test for trigger
UPDATE PitchingAgainst SET H = 171, 2B = 31, 3B = 2, SB = 22, CS = 0, AB = 705, RBI = 66 WHERE playerID LIKE '%reedro01%' AND yearID = 1974 AND stint = 1;

-- Tests for successful update when playerID in Lahman db
SELECT playerID, yearID, stint, TB, TW, SS, TOB, BA, PA, RC
FROM pitchingAnalytics
WHERE playerID = 'reedro01' and yearID = 1974 AND stint = 0;
*/

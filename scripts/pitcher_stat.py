#!/usr/bin/env python3
from dataclasses import dataclass
import sys
import csv
import textwrap
from pathlib import Path
from enum import Enum
from collections import defaultdict
from datetime import datetime
from typing import Any, DefaultDict, Dict, List, Tuple
import pymysql  # type: ignore
import cfg  # type: ignore

MAXYEAR = 2019
MINYEAR = 1974


class E_Record(Enum):
    GAMEID = 0
    BATTING = 1
    PITCHERID = 2
    EVENT_TYPE = 3
    RBI = 4


class G_Record(Enum):
    GAMEID = 0
    VISITOR = 1
    HOME = 2
    SITE = 3
    PITCHES = 4
    V_SCORE = 5
    H_SCORE = 6
    V_HITS = 7
    H_HITS = 8


class P_Type(Enum):
    PITCHERID = 0
    LNAME = 1
    FNAME = 2
    DEBUT = 3


class B_Type(Enum):
    VISITING = 0
    HOME = 1


class E_Type(Enum):
    SO = 3
    SB = 4
    CS = 6
    PO = 8
    PB = 10
    W = 14
    IW = 15
    HBP = 16
    S = 20
    D = 21
    T = 22
    HR = 23


class Stint(Enum):
    TEAMID = 0
    YEAR = 1


class Teams(Enum):
    YEAR = 0
    TEAMID = 1
    LEAGUE = 2


@dataclass
class Stat:
    SO = 0
    SB = 0
    CS = 0
    PO = 0
    PB = 0
    W = 0
    IW = 0
    HBP = 0
    S = 0
    D = 0
    T = 0
    HR = 0
    RBI = 0


games: Dict[str, Dict[str, str]] = {}
teams: Dict[Tuple[str, int], str] = {}
pitcher_stats: DefaultDict[str, DefaultDict[Tuple[str, int], Stat]] = defaultdict(
    lambda: defaultdict(Stat)
)
pitcher: Dict[str, Any] = {}


pitching_against = textwrap.dedent(
    """\
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
    \n\n
    """
)


def load_teams(teams_csv: Path) -> None:
    with open(teams_csv, newline="") as csvfile:
        teamreader = csv.reader(csvfile, delimiter=",", quotechar='"')
        for row in teamreader:
            year = int(row[Teams.YEAR.value])
            team = row[Teams.TEAMID.value]
            league = row[Teams.LEAGUE.value]

            if league == "A":
                teams[(team, year)] = "AL"
            elif league == "N":
                teams[(team, year)] = "NL"


def load_games(games_csv: Path) -> None:
    # read in game data
    with open(games_csv, newline="") as csvfile:
        gamereader = csv.reader(csvfile, delimiter=",", quotechar='"')
        for row in gamereader:
            gameID = row[G_Record.GAMEID.value]
            visitor = row[G_Record.VISITOR.value]
            home = row[G_Record.HOME.value]
            site = row[G_Record.SITE.value]
            pitches = row[G_Record.PITCHES.value]
            v_score = row[G_Record.V_SCORE.value]
            h_score = row[G_Record.H_SCORE.value]
            v_hits = row[G_Record.V_HITS.value]
            h_hits = row[G_Record.H_HITS.value]

            games[gameID] = {
                "visitor": visitor,
                "home": home,
                "site": site,
                "pitches": pitches,
                "v_score": v_score,
                "h_score": h_score,
                "v_hits": v_hits,
                "h_hits": h_hits,
            }


def pitcherID_to_playerID(player_csv: Path) -> None:
    # read in player data
    with open(player_csv, newline="") as csvfile:
        playerreader = csv.reader(csvfile, delimiter=",", quotechar='"')
        for row in playerreader:
            pitcherID = row[P_Type.PITCHERID.value]
            if pitcherID not in pitcher_stats:
                continue

            # a few records do not have first names
            if len(row[P_Type.FNAME.value]) == 0:
                first = None
            else:
                first = row[P_Type.FNAME.value]

            last = row[P_Type.LNAME.value]
            debut_str = row[P_Type.DEBUT.value]
            if len(debut_str) == 0:
                debut = None
            else:
                dt = datetime.strptime(debut_str, "%m/%d/%Y")

                debut = dt.date().isoformat()

            pitcher[pitcherID] = {"first": first, "last": last, "debut": debut}

    connection = pymysql.connect(
        host=cfg.mysql["host"],
        user=cfg.mysql["user"],
        password=cfg.mysql["password"],
        database=cfg.mysql["db"],
    )

    no_debut = "SELECT playerID FROM people WHERE (LOWER(namefirst) LIKE %s OR LOWER(namegiven) LIKE %s) AND LOWER(namelast) LIKE %s;"  # noqa: E501
    full_query = "SELECT playerID FROM people WHERE (LOWER(namefirst) LIKE %s OR LOWER(namegiven) LIKE %s) AND LOWER(namelast) LIKE %s AND debut = %s;"  # noqa: E501
    debut_year = "SELECT playerID FROM people WHERE (LOWER(namefirst) LIKE %s OR LOWER(namegiven) LIKE %s) AND LOWER(namelast) LIKE %s AND YEAR(debut) = %s;"  # noqa: E501

    # automatic closure via context manager
    with connection:
        with connection.cursor() as cursor:
            # best effort to attempt to match people in the retrosheets db
            # with people in the lahman db
            for playerID, innerdict in pitcher.items():
                # default to None
                pitcher[playerID]["playerID"] = None

                # if playerID == 'carmf001' or playerID == 'castf002':
                #     pdb.set_trace()

                if innerdict["debut"] is None and innerdict["first"] is None:
                    sql = no_debut
                    records = cursor.execute(
                        sql,
                        (
                            playerID[4].lower() + "%",
                            playerID[4].lower() + "%",
                            innerdict["last"].lower(),
                        ),
                    )
                elif (
                    innerdict["debut"] is None
                    and innerdict["first"].lower() is not None
                ):
                    sql = no_debut
                    records = cursor.execute(
                        sql,
                        (
                            innerdict["first"].lower(),
                            innerdict["first"].lower(),
                            innerdict["last"].lower(),
                        ),
                    )
                elif innerdict["first"] is None:
                    sql = full_query
                    records = cursor.execute(
                        sql,
                        (
                            playerID[4].lower() + "%",
                            playerID[4].lower() + "%",
                            innerdict["last"].lower(),
                            innerdict["debut"],
                        ),
                    )
                else:
                    sql = full_query
                    records = cursor.execute(
                        sql,
                        (
                            innerdict["first"].lower(),
                            innerdict["first"].lower(),
                            innerdict["last"].lower(),
                            innerdict["debut"],
                        ),
                    )

                if records > 1:
                    # too many records returned with no further way to filter, giving up
                    continue

                if (
                    records == 0
                    and innerdict["debut"] is not None
                    and innerdict["first"] is not None
                ):
                    # try again with just year for debut
                    # this could possibly introduce errors but is highly unlikely
                    sql = debut_year
                    records = cursor.execute(
                        sql,
                        (
                            innerdict["first"].lower(),
                            innerdict["first"].lower(),
                            innerdict["last"].lower(),
                            innerdict["debut"].split("-")[0],
                        ),
                    )
                elif records > 1:
                    # too many records returned with no further way to filter, giving up
                    continue

                if records == 0 and innerdict["debut"] is not None:
                    # try again with just first initial and just year
                    # this could possibly introduce errors but is highly unlikely
                    sql = debut_year
                    records = cursor.execute(
                        sql,
                        (
                            playerID[4].lower() + "%",
                            playerID[4].lower() + "%",
                            innerdict["last"].lower(),
                            innerdict["debut"].split("-")[0],
                        ),
                    )
                elif records > 1:
                    # too many records returned with no further way to filter, giving up
                    continue

                if (
                    records == 0
                    and innerdict["debut"] is not None
                    and innerdict["first"] is not None
                ):
                    # try again with full first but last initial and full debut date
                    # this could possibly introduce errors but is unlikely
                    sql = debut_year
                    records = cursor.execute(
                        sql,
                        (
                            innerdict["first"].lower(),
                            innerdict["first"].lower(),
                            playerID[0].lower() + "%",
                            innerdict["debut"],
                        ),
                    )
                elif records > 1:
                    # too many records returned with no further way to filter, giving up
                    continue

                if records == 1:
                    pitcher[playerID]["playerID"] = cursor.fetchall()[0][0]


def load_pitching_stats(event_csv: Path) -> None:
    # read in event data
    with open(event_csv, newline="") as csvfile:
        eventreader = csv.reader(csvfile, delimiter=",", quotechar='"')
        for row in eventreader:

            pitcherID = row[E_Record.PITCHERID.value]
            gameID = row[E_Record.GAMEID.value]

            # pitcher is on the non-batting team
            batting = int(row[E_Record.BATTING.value])
            if batting == B_Type.HOME.value:
                team = games[gameID]["visitor"]
            else:
                team = games[gameID]["home"]
            year = int(gameID[3:7])
            event = int(row[E_Record.EVENT_TYPE.value])

            rbi = int(row[E_Record.RBI.value])
            pitcher_stats[pitcherID][(team, year)].RBI += rbi

            if event == E_Type.SO.value:
                pitcher_stats[pitcherID][(team, year)].SO += 1
            elif event == E_Type.SB.value:
                pitcher_stats[pitcherID][(team, year)].SB += 1
            elif event == E_Type.CS.value:
                pitcher_stats[pitcherID][(team, year)].CS += 1
            elif event == E_Type.PO.value:
                pitcher_stats[pitcherID][(team, year)].PO += 1
            elif event == E_Type.PB.value:
                pitcher_stats[pitcherID][(team, year)].PB += 1
            elif event == E_Type.W.value:
                pitcher_stats[pitcherID][(team, year)].W += 1
            elif event == E_Type.IW.value:
                pitcher_stats[pitcherID][(team, year)].IW += 1
            elif event == E_Type.HBP.value:
                pitcher_stats[pitcherID][(team, year)].HBP += 1
            elif event == E_Type.S.value:
                pitcher_stats[pitcherID][(team, year)].S += 1
            elif event == E_Type.D.value:
                pitcher_stats[pitcherID][(team, year)].D += 1
            elif event == E_Type.T.value:
                pitcher_stats[pitcherID][(team, year)].T += 1
            elif event == E_Type.HR.value:
                pitcher_stats[pitcherID][(team, year)].HR += 1


def main(games_csv: Path, events_csv: Path, players_csv: Path, teams_csv: Path) -> None:
    print("[-] Loading Games")
    load_games(games_csv)
    print("[+} Games Loaded")
    print("[-] Loading Teams")
    load_teams(teams_csv)
    print("[+] Teams Loaded")
    print("[-] Loading Pitching Stats")
    load_pitching_stats(events_csv)
    print("[+] Pitching Stats Loaded")
    print("[-] Loading PlayerIDs")
    pitcherID_to_playerID(players_csv)
    print("[+] PlayerIDs loaded")

    # TODO: need to add team_ID and FK, looking up ahead of time?
    with open("PitchingAgainst.sql", "w") as f:
        f.write("DROP TABLE IF EXISTS `PitchingAgainst`;\n\n")
        f.write(pitching_against)

        heading = "".join(
            (
                "INSERT INTO `PitchingAgainst` (",
                "`playerID`,`yearID`,`stint`,`teamID`,`lgID`,`SO`,`SB`,`CS`,`PO`,",
                "`PB`,`W`,`IW`,`H`,`2B`,`3B`,`HR`,`RBI`) VALUES ",
            )
        )

        insert = [heading]
        for pitcherID, outerdict in pitcher_stats.items():
            stints: List[int] = []

            for stint, stat in outerdict.items():
                team: str = stint[Stint.TEAMID.value]  # type: ignore
                year: int = stint[Stint.YEAR.value]  # type: ignore
                league = teams[stint]

                stint_num: int = stints.count(year)
                stints.append(year)

                p = pitcher.get(pitcherID, None)
                if p is None:
                    print(f"Could not find: {pitcherID}")
                    continue

                playerID = p["playerID"]
                if playerID is None:
                    continue

                insert.append(
                    "".join(
                        [
                            f"('{playerID}',{year},{stint_num},'{team}','{league}',",
                            f"{stat.SO},{stat.SB},{stat.CS},{stat.PO},{stat.PB},",
                            f"{stat.W},{stat.IW},{stat.S + stat.D + stat.T + stat.HR},",
                            f"{stat.D},{stat.T},{stat.HR},{stat.RBI}),",
                        ]
                    )
                )

        records = "".join(insert)[:-1] + ";\n"
        f.write(records)


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(
            f"Usage: {sys.argv[0]} GAMES.csv EVENTS_INPUT.csv PLAYERS_DEBUT.csv TEAMS.csv"  # noqa: E501
        )
        sys.exit(0)

    games_csv = Path(sys.argv[1])
    if not games_csv.is_file:
        print(f"{sys.argv[1]} is not a file")
        sys.exit(0)

    events_csv = Path(sys.argv[2])
    if not events_csv.is_file:
        print(f"{sys.argv[2]} is not a file")
        sys.exit(0)

    players_csv = Path(sys.argv[3])
    if not players_csv.is_file:
        print(f"{sys.argv[3]} is not a file")
        sys.exit(0)

    teams_csv = Path(sys.argv[4])
    if not teams_csv.is_file:
        print(f"{sys.argv[4]} is not a file")
        sys.exit(0)

    main(games_csv, events_csv, players_csv, teams_csv)

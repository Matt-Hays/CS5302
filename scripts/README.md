# Scripts

## bevent.sh
[bevent.sh](./bevent.sh) - uses BEVENT.EXE to parse the event files looking for pitcher statistics.

When run against all of the event files, this generated **396MB** worth of data.

```
0    game id
14   pitcher
34   event type

    Code Meaning

    0    Unknown event
    1    No event
    2    Generic out
    3    Strikeout
    4    Stolen base
    5    Defensive indifference
    6    Caught stealing
    7    Pickoff error
    8    Pickoff
    9    Wild pitch
    10   Passed ball
    11   Balk
    12   Other advance
    13   Foul error
    14   Walk
    15   Intentional walk
    16   Hit by pitch
    17   Interference
    18   Error
    19   Fielder's choice
    20   Single
    21   Double
    22   Triple
    23   Home run
    24   Missing play
```

## bgame.sh
[bgame.sh](./bgame.sh) - uses BGAME.EXE to parse the event file for game statistics.

When run against all of the eent files, this generated **MB**  worth of data.

```
0    game id
1    date
7    visiting team
8    home team
9    game site
25   pitches entered?
34   visitor final score
35   home final score
36   visitor hits
37   home hits
```

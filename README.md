# mfd-automation
Repository to hold code for MFD automation

Currently, this contains SimpleCombat.py, AlliedNation.csv, and Akatsuki.csv. To run the code, pull the branch, and run on a machine which has python 3.6 or later installed with the pandas and numpy modules installed. Then, from the command line, simple run:

```
python SimpleCombat.py
```

from the directory with SimpleCombat.py, AlliedNation.csv, and Akatsuki.csv in it. A battle log will be printed to the terminal, and the survivors will be put in csv files in AlliedNationPost.csv and AkatsukiPost.csv.

If you'd like to save the battle log, just copy and redirect the output to a file, so, on git bash or unix:

```
python SingleCombat.py | tee BattleLog.log
```

There is also now a mode which can add injuries to the winning side. To use this code, add a death after the call to SingleCombat.py. e.g.

```
python SingleCombat.py death | tee BattleLog.log
```

To adjust the combatants, simply modify the csv files for either AlliendNations or Akatsuki. A data spec for the CSV files follows:

Name -- the name of each ninja. Need not be unique, though more legible if so.

XP -- the total XP the ninja has

Focus -- focus, if any. Combat gives an additional 0.2 multiplier, blank gives no change, anything else gives a -0.2 multiplier

S-ranks -- the number of relevant S-rank techniques this ninja knows -- translates to offensive power bonuses to the tune of an additional 0.1 multiplier per S-rank.

AlliedBuff -- a straight fudge factor on power levels. 0.1 means an additional 0.1 multiplier to power

DefensiveBuffs -- number or intensity of defensive techniques known. This translates to additional health (normally, ninja have 2 health)

Wounds -- Number of wounds a ninja currently has

BuffGiving -- power of buff given to other allies. Note: only gives to allies below themselves in the list

BuffNumber -- number of allies below themselves to apply their BuffGiving to.

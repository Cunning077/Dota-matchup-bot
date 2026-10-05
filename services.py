import re
from heroList import hero_id, hero_name

def parse_mI(string):
    pattern = r"^(.+),\s*(\d+),\s*\[(.*)\]$"

    if not re.match(pattern, string):
        return None

    lane, number, heroes = string.split(",", 2)

    return lane, number, heroes

def calc_winrate(matchups):
    winrates = {}
    for matchup in matchups:
        winrate = matchup['wins'] / matchup['games_played']
        winrates[matchup['hero_id']] = winrate

    return winrates

def calc_avgs(matchSession):
    comb_winrate = {}
    for hero in matchSession:
        for matchup_id, winrate in matchSession[hero]['winrate'].items():
            comb_winrate.setdefault(matchup_id, []).append(winrate)
    avgs = {}
    for winPack in comb_winrate:
        num = 0
        for n in comb_winrate[winPack]:
            num += n
        avg = num / len(comb_winrate[winPack])
        avgs[winPack] = avg
    return avgs

def find_bestPick(avgs):
    bottom_five = sorted(avgs.items(), key=lambda x: x[1])[:5]
    bestPicks = []
    for hero, winrate in bottom_five:
        pick = {'hero': hero_name[hero], 'winrate': winrate}
        bestPicks.append(pick)
    return bestPicks

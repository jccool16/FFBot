import os, dotenv
from discord import Intents, Client
from espn_api.football import League

# load environment vars

dotenv.load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

LEAGUE_ID = int(os.getenv("LEAGUE_ID"))
LEAGUE_YEAR = int(os.getenv("LEAGUE_YEAR"))
ESPN_S2 = os.getenv("ESPN_S2")
SWID = os.getenv("SWID")

# fetch league
print("league fetch started")
league = League(league_id=LEAGUE_ID, year=LEAGUE_YEAR, espn_s2=ESPN_S2, swid=SWID)
print("league fetched")

# setup client
intents: Intents = Intents.default()
client = Client(intents=intents)

# create message
week_num = league.current_week
this_week = league.scoreboard(week_num)
last_week = league.scoreboard(week_num-1)


i = 0
schedule_message = f"""
@everyone Remember to set your lineups this week

We are in Week {league.current_week}

Last week's matchups were:
```ansi
"""
for game in last_week:
    schedule_message += f"\u001b[1;32m{game.home_team.team_name.ljust(25, ' ')}\u001b[0;0m {float(game.home_score)} vs {float(game.away_score)} \u001b[1;31m{game.away_team.team_name.rjust(25, ' ')}\n"
if len(last_week) == 0:
    schedule_message += "No games were played last week\n"
schedule_message += """
```
This week's matchups are:
```ansi
"""
for game in this_week:
    schedule_message += f"\u001b[1;32m{game.home_team.team_name.ljust(29, ' ')}\u001b[0;0m vs \u001b[1;31m{game.away_team.team_name.rjust(29, ' ')}\n"
if len(this_week) == 0:
    schedule_message += "No games are scheduled for this week\n"
schedule_message += """
```
Current Standings:```ansi
"""
for team in league.standings():
    i += 1
    schedule_message += f"""
    \u001b[0;0m {i}. \u001b[1;34m({team.wins}-{team.losses}) \u001b[1;32m {team.team_name}
    """
schedule_message += "```"


schedule_message += f"""
Current Power Rankings:```ansi
"""
i = 0
for team in league.power_rankings():
    i += 1
    schedule_message += f"""
    \u001b[0;0m {i}. \u001b[0;34m{float(team[0])} \u001b[1;32m {team[1].team_name}
    """
schedule_message += "```"

# --- NEW FEATURE: Weekly Top Performers ---
player_stats = []
teams_in_top_5 = set()

for team in league.teams:
    # We check players for the current week
    # Note: .players(week=week_num) retrieves player objects with their weekly stats
    for player in team.roster:
        player_stats.append({
            'name': player.name,
            'points': player.stats[week_num].get('points', 0),
            'team_name': team.team_name
        })

# Sort all players by points descending
player_stats.sort(key=lambda x: x['points'], reverse=True)

# 1. Get the Top 5 global players
top_5_players = player_stats[:5]
for p in top_5_players:
    teams_in_top_5.add(p['team_name'])

# 2. Find best player for teams NOT in the top 5
other_teams_best = []
for team in league.teams:
    if team.team_name not in teams_in_top_5:
        # Find highest scoring player on this specific team
        team_players = [p for p in player_stats if p['team_name'] == team.team_name]
        if team_players:
            best_on_team = max(team_players, key=lambda x: x['points'])
            other_teams_best.append(best_on_team)
all_best_players = top_5_players + other_teams_best
all_best_players.sort(key=lambda x: x['points'], reverse=True)
 
# --- NEW FEATURE: Append Weekly Top Performers to message ---
player_leaderboard_message = "Weekly Top Performers:\n```ansi\n"
if not all_best_players:
    player_leaderboard_message += "No player stats available for this week.\n"
for p in all_best_players:
    player_leaderboard_message += f"\u001b[1;32m{p['name'].ljust(25, ' ')}\u001b[0;0m {float(p['points']):.2f}\n"
player_leaderboard_message += "```"

# startup
@client.event
async def on_ready() -> None:
    print(f"{client.user} is now running")
    channel = client.get_channel(CHANNEL_ID)
    await channel.send(schedule_message)
    await channel.send(player_leaderboard_message)
    await client.close()




def main():
    client.run(token=TOKEN)

if __name__ == "__main__":
    main()

import os, dotenv
from discord import Intents, Client
from espn_api.football import League

# load environment vars

dotenv.load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

LEAGUE_ID = int(os.getenv("LEAGUE_ID"))
ESPN_S2 = os.getenv("ESPN_S2")
SWID = os.getenv("SWID")

# fetch league
print("league fetch started")
league = League(league_id=LEAGUE_ID, year=2024, espn_s2=ESPN_S2, swid=SWID)
print("league fetched")

# setup client
intents: Intents = Intents.default()
client = Client(intents=intents)

# create message
week_num = league.current_week
this_week = league.scoreboard(week_num)
last_week = league.scoreboard(week_num-1)


i = 0
message = f"""
@everyone Remember to set your lineups this week

We are in Week {league.current_week}

Last week's matchups were:
```ansi
\u001b[1;32m{last_week[0].home_team.team_name.ljust(25, " ")}\u001b[0;0m {float(last_week[0].home_score)} vs {float(last_week[0].away_score)} \u001b[1;31m{last_week[0].away_team.team_name.rjust(25, " ")}

\u001b[1;32m{last_week[1].home_team.team_name.ljust(25, " ")}\u001b[0;0m {float(last_week[1].home_score)} vs {float(last_week[1].away_score)} \u001b[1;31m{last_week[1].away_team.team_name.rjust(25, " ")}

\u001b[1;32m{last_week[2].home_team.team_name.ljust(25, " ")}\u001b[0;0m {float(last_week[2].home_score)} vs {float(last_week[2].away_score)} \u001b[1;31m{last_week[2].away_team.team_name.rjust(25, " ")}

\u001b[1;32m{last_week[3].home_team.team_name.ljust(25, " ")}\u001b[0;0m {float(last_week[3].home_score)} vs {float(last_week[3].away_score)} \u001b[1;31m{last_week[3].away_team.team_name.rjust(25, " ")}
```
This week's matchups are:
```ansi
\u001b[1;32m{this_week[0].home_team.team_name.ljust(25, " ")}\u001b[0;0m vs \u001b[1;31m{this_week[0].away_team.team_name.rjust(25, " ")}

\u001b[1;32m{this_week[1].home_team.team_name.ljust(25, " ")}\u001b[0;0m vs \u001b[1;31m{this_week[1].away_team.team_name.rjust(25, " ")}

\u001b[1;32m{this_week[2].home_team.team_name.ljust(25, " ")}\u001b[0;0m vs \u001b[1;31m{this_week[2].away_team.team_name.rjust(25, " ")}

\u001b[1;32m{this_week[3].home_team.team_name.ljust(25, " ")}\u001b[0;0m vs \u001b[1;31m{this_week[3].away_team.team_name.rjust(25, " ")}
```
Current Standings:```ansi
"""
for team in league.standings():
    i += 1
    message += f"""
    \u001b[0;0m {i}. \u001b[1;34m({team.wins}-{team.losses}) \u001b[1;32m {team.team_name}
    """
message += "```"


message += f"""
Current Power Rankings:```ansi
"""
i = 0
for team in league.power_rankings():
    i += 1
    message += f"""
    \u001b[0;0m {i}. \u001b[0;34m{float(team[0])} \u001b[1;32m {team[1].team_name}
    """
message += "```"



# startup
@client.event
async def on_ready() -> None:
    print(f"{client.user} is now running")
    channel = client.get_channel(CHANNEL_ID)
    await channel.send(message)
    await client.close()




def main():
    client.run(token=TOKEN)

if __name__ == "__main__":
    main()
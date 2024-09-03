import os, dotenv
from discord import Intents, Client

# load environment vars

dotenv.load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# setup

intents: Intents = Intents.default()
client = Client(intents=intents)

message = """@reminders Set your lineups"""

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
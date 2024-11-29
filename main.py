from Extensions.utilities import interactions_bot
from constants import *

@listen()
async def on_ready():
	print("Ready")
	print(f"Logged in as {interactions_bot.user}")

for extension in EXTENSIONS:
	interactions_bot.load_extension(extension)

if __name__ == "__main__":
	interactions_bot.start()
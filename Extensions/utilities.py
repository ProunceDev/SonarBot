from constants import *
from interactions import *
from dotenv import load_dotenv

load_dotenv()

interactions_bot = Client(debug_scope=1182145582119256084, intents=Intents.ALL, token=os.getenv("discord_token"))

class Utilities(Extension):
	pass


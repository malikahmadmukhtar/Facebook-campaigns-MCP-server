import os
from dotenv import load_dotenv

load_dotenv()

OPEN_WEATHER_KEY=os.getenv("OPEN_WEATHER_KEY")

## facebook setup
fb_access_token = os.getenv("FB_ACCESS_TOKEN")
fb_base_url = os.getenv("FB_BASE_URL")

SERVER_NAME = "myserver"
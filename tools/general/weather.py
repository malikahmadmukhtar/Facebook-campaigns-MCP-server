import requests
from config.settings import OPEN_WEATHER_KEY
from utils.server import myserver


@myserver.tool()
async def get_weather_by_city(city_name: str) -> str:
    """
    Get the current weather for a given city.
    Always ask the user for a city first.

    Args:
        city_name (str): The name of the city.

    Returns:
        str: Weather information like temperature, description, humidity, and wind speed etc.
    """
    print("Used weather tool")

    api_key = OPEN_WEATHER_KEY
    base_url = "http://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric"
    }

    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            return (
                f"Weather in {data['name']}:\n"
                f"- Temperature: {data['main']['temp']}°C\n"
                f"- Description: {data['weather'][0]['description']}\n"
                f"- Humidity: {data['main']['humidity']}%\n"
                f"- Wind Speed: {data['wind']['speed']} m/s"
            )
        else:
            return f"Error: City not found or API error ({response.status_code})"
    except Exception as e:
        return f"Exception occurred: {str(e)}"

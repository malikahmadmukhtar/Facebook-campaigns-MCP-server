import requests
from config.settings import fb_access_token, fb_base_url
from utils.server import myserver


@myserver.tool()
def search_interests(query: str) -> list:
    """
    Search for Facebook interest targeting options based on a keyword.

    Use this tool to get interest IDs and names for use in ad set targeting.
    Each interest will include an `id` and `name` field. You can use the top results to build your targeting.

    Parameters:
    - query: A keyword or phrase (e.g., "Marketing", "Technology", "Fitness")

    Returns:
    - A list of matching interest dicts with `id` and `name`
    """

    print("Search interest called")

    url = f'{fb_base_url}search'
    params = {
        'type': 'adinterest',
        'q': query,
        'access_token': fb_access_token,
        'limit': 5
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get('data', [])
    except requests.exceptions.RequestException as e:
        return [{"error": f"Error searching interests: {str(e)}"}]



@myserver.tool()
def get_behavior_ids() -> dict:
    """
    Get a dictionary of common Facebook behavior targeting options.

    Use this tool to look up behavior IDs when creating or editing ad sets.
    You can reference this mapping to provide appropriate `id` and `name` pairs for targeting.

    Returns:
    - A dictionary where keys are behavior names and values are their corresponding Facebook behavior IDs.
    """
    print("Get behaviour ids called")

    return {
        "Small Business Owners": "6071631541183",
        "Frequent Travelers": "6002714895372",
        "Frequent International Travelers": "6003139266461",
        "Frequent Luxury Travelers": "6003409043876",
        "Frequent Business Travelers": "6003020834694",
        "Frequent Domestic Travelers": "6002714898572",
        "Frequent Travelers - All Types": "6002714895372"
    }


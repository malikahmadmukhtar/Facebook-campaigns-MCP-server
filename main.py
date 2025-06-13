import os
from utils.server import myserver
from tools.general.weather import get_weather_by_city
from tools.facebook import accounts, campaigns, catalogs, products, adsets, ad_creative, catalog_creative, pages, helpers, facebook_ads


## for local

# if __name__ == "__main__":
#     # Initialize and run the server
#     myserver.run(transport='stdio')


## for hosting

if __name__ == "__main__":
    # Get the port from an environment variable (common for web hosting)
    # Default to 8000 for local development if the environment variable isn't set.
    port = int(os.environ.get("PORT", 8000))

    print(f"Starting FastMCP server on http://0.0.0.0:{port} using streamable_http transport...")
    # Change 'stdio' to 'streamable_http' for web deployment
    # 'host="0.0.0.0"' makes it accessible from external connections (required for web)
    myserver.run(transport='streamable_http', host="0.0.0.0", port=port)
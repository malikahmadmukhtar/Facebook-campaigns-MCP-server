import json
from typing import Any, Dict, Union, List
import requests
from config.settings import fb_base_url, fb_access_token
from utils.server import myserver


@myserver.tool()
def fetch_products_from_catalog(catalog_id: str) -> str:
    """
    Fetches all products from a Facebook catalog by catalog ID.
    Products will be shown to the user with their name, description, price, and image URL.
    """
    print(f"Tool Called: fetch_products_from_catalog with catalog_id: {catalog_id}")

    products: List[Dict[str, Any]] = []
    base_url = f"{fb_base_url}{catalog_id}/products"
    params: Dict[str, Union[str, int]] = {
        'access_token': fb_access_token,
        'fields': 'id,name,description,price,image_url,url,availability',
        'limit': 100
    }

    # Helper function to construct a JSON-RPC error response
    def _create_error_response(message: str, code: int = -32000, data: Any = None) -> str:
        error_payload: Dict[str, Any] = {
            "jsonrpc": "2.0",
            "id": None,  # In a full JSON-RPC implementation, you'd echo the request ID here
            "error": {
                "code": code,
                "message": message
            }
        }
        if data is not None:
            error_payload["error"]["data"] = data
        return json.dumps(error_payload)

    try:
        while True:
            response = requests.get(base_url, params=params)
            response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
            data: Dict[str, Any] = response.json()

            # Check for Facebook API specific errors embedded in the response body
            if 'error' in data:
                fb_error = data['error']
                return _create_error_response(
                    message=f"Facebook API Error: {fb_error.get('message', 'Unknown API error')}",
                    data=fb_error
                )

            products.extend(data.get('data', []))

            next_page = data.get('paging', {}).get('next')
            if not next_page:
                break  # No more pages

            base_url = next_page  # Use the full URL for the next page

        if not products:
            # Construct JSON-RPC success response for no products found
            success_payload_no_products: Dict[str, Any] = {
                "jsonrpc": "2.0",
                "id": None,
                "result": {
                    "content": [],
                    "isError": False,
                    "message": "No products found in this catalog."
                }
            }
            return json.dumps(success_payload_no_products)

        # Transform each product dictionary into the nested 'text' format
        content_array: List[Dict[str, str]] = [
            {"type": "text", "text": json.dumps(product_dict)}
            for product_dict in products
        ]

        # Construct the final JSON-RPC success response
        final_success_payload: Dict[str, Any] = {
            "jsonrpc": "2.0",
            "id": None,  # Still using None; ideally, this comes from the incoming request
            "result": {
                "content": content_array,
                "isError": False
            }
        }

        # print(f"\nTool output (before final JSON.dumps): {final_success_payload}") # Debug print
        return json.dumps(final_success_payload)

    except requests.exceptions.HTTPError as http_err:
        # Catches 4xx or 5xx responses from requests.raise_for_status()
        return _create_error_response(
            message=f"HTTP Error during Facebook API call: {http_err.response.status_code} - {http_err.response.text}",
            code=http_err.response.status_code
        )
    except requests.exceptions.ConnectionError as conn_err:
        # Catches network-related errors (e.g., DNS failure, refused connection)
        return _create_error_response(
            message=f"Network connection error during Facebook API call: {str(conn_err)}",
            code=-32002  # Custom code for connection errors
        )
    except requests.exceptions.Timeout as timeout_err:
        # Catches request timeout errors
        return _create_error_response(
            message=f"Request timed out during Facebook API call: {str(timeout_err)}",
            code=-32003  # Custom code for timeouts
        )
    except requests.exceptions.RequestException as req_err:
        # Catch any other requests-related exceptions
        return _create_error_response(
            message=f"An unexpected requests error occurred: {str(req_err)}",
            code=-32004  # Custom code for general requests errors
        )
    except json.JSONDecodeError as json_err:
        # Catches errors if response is not valid JSON
        return _create_error_response(
            message=f"Failed to decode JSON response from Facebook API: {str(json_err)}",
            code=-32005  # Custom code for JSON decoding errors
        )
    except Exception as e:
        # Catch any other unexpected errors
        return _create_error_response(
            message=f"An unexpected error occurred in the tool: {str(e)}",
            code=-32006  # Generic internal error code
        )


# @myserver.tool()
# def fetch_products_from_catalog(catalog_id: str) -> str | list[Any]:
#     """
#     Fetches all products from a Facebook catalog by catalog ID not the name which can get using the get_facebook_catalogs tool while following its structure.
#     Show the list of catalogs and let the user choose the catalog then fetch based on user choice.
#     Products will be shown to user with their name, description, price and image URL.
#     """
#
#     print(f"Tool Called: fetch_products_from_catalog")
#     base_url = f"{fb_base_url}{catalog_id}/products"
#     products = []
#     params = {
#         'access_token': fb_access_token,
#         'fields': 'id,name,description,price,image_url,url,availability',
#         'limit': 100
#     }
#
#     try:
#         while True:
#             response = requests.get(base_url, params=params)
#             print(response.json())
#             data = response.json()
#
#             if 'error' in data:
#                 error = data['error']
#                 return f"Facebook API Error: {error['message']}"
#
#             products.extend(data.get('data', []))
#
#             next_page = data.get('paging', {}).get('next')
#             if not next_page:
#                 break
#
#             # For next page, use full URL (Graph API includes access_token in it)
#             base_url = next_page
#
#         if not products:
#             return "No products found in this catalog."
#
#         print(f"\nproducts tool output {str(products)}")
#         return json.dumps(products)
#         # return f"Fetched {len(products)} products from catalog {catalog_id} which are {products}."
#         # return response.json()
#
#     except Exception as e:
#         return f"An error occurred: {str(e)}"



@myserver.tool()
def delete_catalog_product(product_id: str) -> str:
    """
    Deletes a product from a Facebook catalog by its product ID.
    First show the products with their ids and then ask user to choose which product to delete.
    """

    url = f'{fb_base_url}{product_id}'
    params = {
        'access_token': fb_access_token
    }

    try:
        response = requests.delete(url, params=params)
        response.raise_for_status()
        success = response.json().get('success', False)
        if success:
            return f"Product {product_id} deleted successfully."
        else:
            return f"Product deletion request was received but not confirmed."
    except requests.exceptions.RequestException as e:
        return f"Error deleting product: {str(e)}"


# @myserver.tool()
# def start_catalog_product_creation(
#     catalog_id: str,
#     ad_account_id: str | None = None,
#     name: str | None = None,
#     description: str | None = None,
#     price: float | None = None,
#     url: str | None = None,
#     availability: str | None = None,
# ) -> str:
#     """
#     Creates a new product in the selected Facebook catalog and collects all required information via user prompts.
#
#     DO NOT hardcode any data or assume values. Instead:
#     - Ask the user for all the data like (name, description, price and availability) before using this tool.
#     - Use the 'get_facebook_catalogs' tool to get the catalog ID (ask the user to select from the results).
#     - Use the 'get_facebook_ad_accounts' tool to fetch the currency (based on ad_account_id).
#
#     Parameters:
#     - catalog_id: ID of the Facebook catalog (fetched using 'get_facebook_catalogs'; do not use the name).
#     - ad_account_id: The ad account ID (not business ID) used to retrieve currency info.
#     - name: Name of the product (ask the user).
#     - description: Description of the product (ask the user).
#     - price: Product price (as a float, in the currency of the ad account; ask the user).
#     - url: Product page URL (ask the user).
#     - availability: Product availability status. Must be one of:
#       ["in stock", "out of stock", "available for order", "discontinued"].
#
#     Returns:
#     - Message to upload image after calling this tool with correct data or an error if data is invalid.
#     """
#
#     required_fields = {
#         "catalog_id": catalog_id,
#         "ad_account_id": ad_account_id,
#         "name": name,
#         "description": description,
#         "price": price,
#         "url": url,
#         "availability": availability,
#     }
#
#     # Check for any missing or invalid fields
#     missing = [field for field, value in required_fields.items() if not value]
#     if missing:
#         return f"Missing required product fields: {', '.join(missing)}. Please provide all required data."
#     else:
#         st.session_state.pending_product = {
#             "catalog_id": catalog_id,
#             "ad_account_id": ad_account_id,
#             "name": name,
#             "description": description,
#             "price": price,
#             "url": url,
#             "availability": availability.lower()
#         }
#
#         return "Product details received. Please upload a product image to complete catalog product creation."

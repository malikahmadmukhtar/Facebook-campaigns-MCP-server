import os
from mcp.server.fastmcp import FastMCP
from config.settings import SERVER_NAME

# myserver = FastMCP(SERVER_NAME)

port = int(os.environ.get("PORT", 8000))

# Listen on all available network interfaces for Render deployment
host = "0.0.0.0"

# The path for the 'streamable-http' transport as per official docs
path = "/mcp"

# Pass host, port, and path directly to the FastMCP constructor
# FastMCP is designed to accept these as part of its initial configuration
myserver = FastMCP(
    SERVER_NAME,
    host=host,
    port=port,
    path=path
)

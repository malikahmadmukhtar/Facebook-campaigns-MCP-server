#!/usr/bin/env bash

# This script will be executed by Render to start your application.
# It tells Uvicorn to run your FastMCP server.

# Replace 'your_server_file_name' with the actual name of your Python file
# (e.g., if your code is in 'app.py', use 'app')
# 'myserver.app' refers to the FastMCP instance's underlying ASGI app.
# $PORT is an environment variable provided by Render.
uvicorn main:app --host 0.0.0.0 --port $PORT
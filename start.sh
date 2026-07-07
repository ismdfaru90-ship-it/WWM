#!/bin/bash
set -e

# Install dependencies
cd /app
pip install -e .

# Set environment variables
export PYTHONPATH="/app"
export SERVE_FRONTEND="true"

# Start the server
uvicorn openhands.app_server.app:app --host 0.0.0.0 --port 3000

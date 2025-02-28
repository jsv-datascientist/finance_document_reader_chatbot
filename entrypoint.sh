#!/bin/sh

# Set a default port if not provided
PORT=${PORT:-8000}

# Start the FastAPI app
exec uvicorn api.api:app --host 0.0.0.0 --port "$PORT"

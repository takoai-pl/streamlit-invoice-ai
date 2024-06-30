#!/bin/bash

if [ -f .env ]; then
    echo ".env file found, loading..."

    # Export variables directly from the .env file
    set -a
    source .env
    set +a

    echo ".env file loaded and variables exported."
else
    echo ".env file not found, continuing without it..."
fi
# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Install FastAPI, Uvicorn and curl
RUN pip install fastapi uvicorn && apt-get update && apt-get install -y curl

# Set the WORKDIR to /app so all following commands run in /app
WORKDIR /app

# Copy the server.py file into the current directory (/app)
COPY ./server.py .

# Expose port 8000 for the FastAPI server to listen on
EXPOSE 8000

# Start the FastAPI server on 0.0.0.0 so it listens on all interfaces
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]

# Healthcheck instruction
HEALTHCHECK CMD curl --fail http://localhost:8000/docs || exit 1
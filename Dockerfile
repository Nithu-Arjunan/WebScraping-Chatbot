# Use official Python image
FROM python:3.11-slim-bookworm

# Set working directory
WORKDIR /app

# Copy everything from root to /app (ignoring things in .dockerignore)
COPY . .

# patch OS, install dos2unix
RUN apt-get update \
 && apt-get install -y --no-install-recommends dos2unix \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

 # convert line endings & make executable
RUN dos2unix /app/entrypoint.sh

# Optional: Patch known vulnerabilities at the OS level
RUN apt-get update && apt-get upgrade -y && apt-get clean

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose ports for FastAPI and Streamlit
EXPOSE  8501

# Make entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Start both backend and frontend when container starts
CMD ["/app/entrypoint.sh"]

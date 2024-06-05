# Build stage
FROM python:3.10-slim as build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Create a virtual environment
RUN python3 -m venv /venv

# Activate the virtual environment
ENV PATH="/venv/bin:$PATH"

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application

COPY . .

# Final stage
FROM python:3.10-slim

# Install PostgreSQL client library
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd --create-home appuser

# Set the working directory
WORKDIR /app

# Copy the application code and dependencies
COPY --from=build /app /app
COPY --from=build /venv /venv

# Chown the app directory and virtual environment
RUN chown -R appuser:appuser /app /venv

# Switch to the non-root user
USER appuser

# Activate the virtual environment
ENV PATH="/venv/bin:$PATH"

# Expose the port the app runs on
EXPOSE 5000

# Set the environment variables
ENV DB_HOST=your_db_host \
    DB_NAME=your_db_name \
    DB_USER=your_db_user \
    DB_PASSWORD=your_db_password \
    SECRET_KEY=your_secret_key

# Start the Flask application
CMD ["python", "app.py"]
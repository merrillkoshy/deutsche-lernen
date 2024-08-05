# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables to ensure output is not buffered
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000
EXPOSE 8000

# Define environment variable
ENV NAME FastAPIApp

# Run the application
CMD ["uvicorn", "app.main:fastapp", "--host", "0.0.0.0", "--port", "8000"]

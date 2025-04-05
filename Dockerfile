# Use an official Python base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install OS-level dependencies required for dlib
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    libboost-all-dev \
    && apt-get clean

# Set working directory
WORKDIR /app

# Copy project files into container
COPY . /app/

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port the app runs on (optional)
EXPOSE 8000

# Run your application (change this to your app’s entry point)
CMD ["python", "app.py"]

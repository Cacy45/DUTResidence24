# Stage 1: Build the Django application
FROM python:3.9 AS build

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Stage 2: Set up Nginx and copy the Django application
FROM nginx:alpine

# Install supervisord
RUN apk add --no-cache supervisor

# Copy the built Django application from the first stage
COPY --from=build /app /app

# Copy Nginx configuration file
COPY nginx.conf /etc/nginx/nginx.conf

# Copy supervisord configuration file
COPY supervisord.conf /etc/supervisord.conf

# Expose the port Nginx will run on
EXPOSE 80

# Start supervisord
CMD ["supervisord", "-c", "/etc/supervisord.conf"]
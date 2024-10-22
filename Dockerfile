# Stage 1: Build the Django application
FROM python:3.12 AS build

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

# Install Tini
RUN apk add --no-cache tini

# Copy the built Django application from the first stage
COPY --from=build /app /app

# Copy Nginx configuration file
COPY nginx.conf /etc/nginx/nginx.conf

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose the port Nginx will run on
EXPOSE 80

# Use Tini as the entrypoint
ENTRYPOINT ["/sbin/tini", "--"]

# Start the services
CMD ["/entrypoint.sh"]
# Use the latest Debian image as the base
FROM debian:latest

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       python3 \
       python3-pip \
       nginx \
       tini \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt ./

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Copy Nginx configuration file
COPY nginx.conf /etc/nginx/nginx.conf

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose the port Nginx will run on
EXPOSE 80

# Use Tini as the entrypoint
ENTRYPOINT ["/usr/bin/tini", "--"]

# Start the services
CMD ["/entrypoint.sh"]
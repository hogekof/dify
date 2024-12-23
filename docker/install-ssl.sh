#!/bin/bash

# Check if install-ssl.sh exists in the current directory
if [ ! -f "./install-ssl.sh" ]; then
    echo "Error: install-ssl.sh not found in the current directory."
    exit 1
fi

# Check if email and domain parameters are provided
if [ $# -ne 2 ]; then
    echo "Usage: $0 <email> <domain>"
    exit 1
fi

EMAIL=$1
DOMAIN=$2

# Update .env
sed -i 's/^NGINX_SSL_CERT_FILENAME=.*/NGINX_SSL_CERT_FILENAME=fullchain.pem/' .env
sed -i 's/^NGINX_SSL_CERT_KEY_FILENAME=.*/NGINX_SSL_CERT_KEY_FILENAME=privkey.pem/' .env
sed -i 's/^NGINX_ENABLE_CERTBOT_CHALLENGE=.*/NGINX_ENABLE_CERTBOT_CHALLENGE=true/' .env
sed -i "s/^CERTBOT_DOMAIN=.*/CERTBOT_DOMAIN=$DOMAIN/" .env
sed -i "s/^CERTBOT_EMAIL=.*/CERTBOT_EMAIL=$EMAIL/" .env

# Update SERVICE_API_URL and APP_WEB_URL
sed -i "s|^SERVICE_API_URL=.*|SERVICE_API_URL=https://$DOMAIN|" .env
sed -i "s|^APP_WEB_URL=.*|APP_WEB_URL=https://$DOMAIN|" .env

# Prune Docker networks and start containers
sudo docker network prune -f
sudo docker compose -f docker-compose.yaml --profile certbot up --force-recreate -d

# Run certbot
sudo docker compose -f docker-compose.yaml exec -T certbot /bin/sh /update-cert.sh

# Enable HTTPS
sed -i 's/^NGINX_HTTPS_ENABLED=.*/NGINX_HTTPS_ENABLED=true/' .env

# Recreate nginx container
sudo docker compose -f docker-compose.yaml --profile certbot up -d --no-deps --force-recreate nginx

echo "Dify installation with SSL is complete. Please check https://$DOMAIN"

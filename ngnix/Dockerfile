# Base image
FROM nginx:alpine

# Copy your custom Nginx configuration file
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf

# Create a volume for static files (this will be shared with Django)
VOLUME /static

# Expose port 80 for Nginx
EXPOSE 80

FROM python:3.9-alpine

USER Root

WORKDIR /var/Trading_App/Django_back_end

COPY . /var/Trading_App/Django_back_end

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Nginx
RUN apt-get update && apt-get install -y nginx
COPY nginx/nginx.conf /etc/nginx/nginx.conf

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the Nginx port
EXPOSE 80

# Run Nginx and Gunicorn
CMD ["sh", "-c", "nginx && gunicorn your_django_app.wsgi:application --bind 0.0.0.0:8000"]

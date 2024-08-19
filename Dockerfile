FROM python:3.10-alpine

WORKDIR /var/Trading_App/Django_back_end

COPY Django_back_end /var/Trading_App/Django_back_end/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Collect static files
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Expose the Nginx port
EXPOSE 80

# Run server with Gunicorn
CMD ["gunicorn", "TradingBotProj1.wsgi:application", "--bind", "0.0.0.0:8000"]

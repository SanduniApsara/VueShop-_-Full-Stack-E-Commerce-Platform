FROM python:3.11-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput --settings=vueshop.settings.production || true

EXPOSE 8000

CMD ["gunicorn", "vueshop.wsgi:application", "--bind", "0.0.0.0:8000"]

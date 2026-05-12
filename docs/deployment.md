# Deployment Guide

## Prerequisites
- A Linux VPS (Ubuntu 22.04 recommended)
- Docker & Docker Compose installed
- A domain name (optional but recommended)

## Steps

### 1. Clone and configure
```bash
git clone https://github.com/YOUR_USERNAME/vueshop.git
cd vueshop

# Backend env
cp backend/.env.example backend/.env
nano backend/.env   # fill in production values

# Frontend env
cp frontend/.env.example frontend/.env.local
nano frontend/.env.local
```

### 2. Build and start
```bash
docker-compose up --build -d
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py loaddata fixtures/sample_data.json
```

### 3. SSL with Let's Encrypt (optional)
Install Certbot and update `nginx.conf` with your domain and SSL certificate paths.

```bash
sudo apt install certbot
sudo certbot certonly --standalone -d yourdomain.com
```

## Environment Variables Reference

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Django secret key |
| `DB_NAME` | PostgreSQL database name |
| `DB_USER` | PostgreSQL user |
| `DB_PASSWORD` | PostgreSQL password |
| `STRIPE_SECRET_KEY` | Stripe secret key |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts |
| `CORS_ALLOWED_ORIGINS` | Frontend URL for CORS |

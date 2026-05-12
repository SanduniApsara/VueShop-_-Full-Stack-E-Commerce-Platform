# 🛍️ VueShop — Full-Stack E-Commerce Platform

> A production-ready e-commerce application built with **Vue.js 3**, **Bootstrap 5**, **Tailwind CSS**, and **Django REST Framework**.

![VueShop Banner](https://img.shields.io/badge/Vue.js-3.x-4FC08D?style=for-the-badge&logo=vue.js)
![Django](https://img.shields.io/badge/Django-4.x-092E20?style=for-the-badge&logo=django)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.x-7952B3?style=for-the-badge&logo=bootstrap)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.x-06B6D4?style=for-the-badge&logo=tailwindcss)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

---

## ✨ Features

### 🛒 Storefront
- Product listing with filters, search, and sorting
- Product detail pages with image gallery
- Shopping cart with real-time quantity updates
- Wishlist functionality
- Category & tag browsing

### 💳 Checkout & Orders
- Multi-step checkout (Address → Shipping → Payment → Confirmation)
- Stripe payment integration
- Order history and tracking
- Email order confirmations

### 👤 User Experience
- JWT-based authentication (Register / Login / Logout)
- User profile & address management
- Product reviews & star ratings
- Responsive design (mobile-first)

### 🔧 Admin / Backend
- Django Admin panel for product & order management
- REST API with DRF (Django REST Framework)
- Product CRUD with image uploads
- Inventory & stock tracking
- Sales analytics endpoint

---

## 🏗️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend Framework** | Vue.js 3 (Composition API) |
| **State Management** | Pinia |
| **UI Components** | Bootstrap 5 + Tailwind CSS |
| **HTTP Client** | Axios |
| **Router** | Vue Router 4 |
| **Backend** | Django 4 + Django REST Framework |
| **Auth** | JWT (djangorestframework-simplejwt) |
| **Database** | PostgreSQL (SQLite for dev) |
| **Payments** | Stripe |
| **Storage** | Django media / AWS S3 (prod) |
| **Deployment** | Docker + Nginx |

---

## 📁 Project Structure

```
vueshop/
├── backend/                    # Django project
│   ├── vueshop/               # Django settings & config
│   │   ├── settings/
│   │   │   ├── base.py
│   │   │   ├── development.py
│   │   │   └── production.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── shop/                  # Main app
│   │   ├── models.py          # Product, Order, Cart, Review
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── admin.py
│   ├── accounts/              # User auth app
│   ├── requirements.txt
│   └── manage.py
│
├── frontend/                   # Vue.js project
│   ├── src/
│   │   ├── components/
│   │   │   ├── layout/        # Navbar, Footer, Sidebar
│   │   │   ├── product/       # ProductCard, ProductGrid, etc.
│   │   │   ├── cart/          # CartDrawer, CartItem
│   │   │   ├── checkout/      # CheckoutSteps, PaymentForm
│   │   │   └── auth/          # LoginForm, RegisterForm
│   │   ├── views/             # Page-level components
│   │   ├── store/             # Pinia stores
│   │   ├── router/            # Vue Router config
│   │   ├── assets/            # CSS, images
│   │   └── main.js
│   ├── public/
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
├── docker-compose.yml
├── nginx.conf
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL (or use SQLite for dev)

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/vueshop.git
cd vueshop
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Run migrations
python manage.py migrate

# Load sample data
python manage.py loaddata fixtures/sample_data.json

# Create superuser
python manage.py createsuperuser

# Start Django server
python manage.py runserver
```

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env.local
# Set VITE_API_BASE_URL=http://localhost:8000

# Start dev server
npm run dev
```

### 4. Access the app
| Service | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000/api/ |
| Admin Panel | http://localhost:8000/admin/ |
| API Docs | http://localhost:8000/api/docs/ |

---

## 🐳 Docker Setup

```bash
# Build and run all services
docker-compose up --build

# Run migrations inside container
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
```

---

## 🔌 API Endpoints

### Products
```
GET    /api/products/              List all products
GET    /api/products/{id}/         Product detail
GET    /api/products/featured/     Featured products
GET    /api/categories/            All categories
```

### Cart & Orders
```
GET    /api/cart/                  Get user cart
POST   /api/cart/add/              Add item to cart
PUT    /api/cart/update/{id}/      Update quantity
DELETE /api/cart/remove/{id}/      Remove item
POST   /api/orders/                Create order
GET    /api/orders/                User order history
GET    /api/orders/{id}/           Order detail
```

### Auth
```
POST   /api/auth/register/         Register user
POST   /api/auth/login/            Login (get JWT)
POST   /api/auth/token/refresh/    Refresh JWT
GET    /api/auth/profile/          User profile
```

---

## 🎨 Screenshots

> Add your screenshots here after running the project!

---

## 🧪 Running Tests

```bash
# Backend tests
cd backend
python manage.py test

# Frontend tests
cd frontend
npm run test
```

---

## 📦 Deployment

See [docs/deployment.md](docs/deployment.md) for production deployment instructions with:
- Nginx reverse proxy config
- Gunicorn setup
- SSL/HTTPS with Let's Encrypt
- PostgreSQL configuration
- Environment variables reference

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

Built with ❤️ for real-world use. Star ⭐ the repo if you find it useful!

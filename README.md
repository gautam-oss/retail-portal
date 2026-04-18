# Retail Portal — Django Full Stack Project

> A robust, scalable e-commerce platform built with Django 6, Tailwind CSS, pg_trgm fuzzy search, role-based access control, Django REST Framework, and JWT authentication.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Repository Structure](#2-repository-structure)
3. [Tech Stack](#3-tech-stack)
4. [Features](#4-features)
5. [API Design](#5-api-design)
6. [Auth & Roles](#6-auth--roles)
7. [Running the Project](#7-running-the-project)
8. [Environment Variables](#8-environment-variables)

---

## 1. Project Overview

A full-stack e-commerce platform that handles:

- **User management** — registration, login, role-based access (Admin / Customer)
- **Product & category management** — full CRUD with image uploads
- **Shopping experience** — fuzzy search, pagination, order history, re-ordering
- **API layer** — Django REST Framework with JWT for headless/mobile clients

Built with Django 6 server-side rendered templates + DRF API, PostgreSQL, and Docker.

---

## 2. Repository Structure

```
retail-portal/
├── core/                        # Project settings, root URLs, WSGI
│   ├── settings.py
│   ├── urls.py
│   ├── views.py
│   └── wsgi.py
│
├── accounts/                    # Auth, login, register, roles
│   ├── migrations/
│   ├── templates/accounts/
│   │   ├── login.html
│   │   ├── register.html
│   │   └── profile.html
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
│
├── categories/                  # Category management
│   ├── migrations/
│   ├── templates/categories/
│   │   ├── list.html
│   │   ├── form.html
│   │   └── confirm_delete.html
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
│
├── products/                    # Product CRUD, stock, images
│   ├── migrations/
│   ├── templates/products/
│   │   ├── list.html
│   │   ├── detail.html
│   │   ├── form.html
│   │   ├── stock_form.html
│   │   └── confirm_delete.html
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
│
├── orders/                      # Orders, history, re-ordering
│   ├── migrations/
│   ├── templates/orders/
│   │   ├── list.html
│   │   └── detail.html
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
│
├── search/                      # pg_trgm fuzzy search
│   ├── templates/search/
│   │   └── results.html
│   ├── urls.py
│   └── views.py
│
├── templates/                   # Global base templates
│   ├── base.html
│   ├── navbar.html
│   ├── footer.html
│   └── home.html
│
├── static/
│   ├── css/main.css
│   └── js/main.js
│
├── media/                       # User-uploaded files
│
├── .github/
│   └── workflows/
│       └── deploy.yml           # GitHub Actions CI/CD
│
├── render.yaml
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── nginx.conf
├── .env.example
└── manage.py
```

---

## 3. Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 6.0 |
| API | Django REST Framework 3.17 |
| Frontend | Django Templates + Tailwind CSS (CDN) |
| Database | PostgreSQL 16 |
| Auth | Django session auth + JWT (simplejwt) |
| Fuzzy Search | `pg_trgm` — PostgreSQL trigram extension |
| Static Files | WhiteNoise + Django `staticfiles` |
| CI/CD | GitHub Actions |
| Deployment | Docker + Gunicorn + Nginx + Render |

---

## 4. Features

### User & Auth
- User sign-up & login (Django session auth + JWT for API)
- Role-Based Access Control: **Admin** and **Customer**
- Protected views with `@login_required` and role checks
- JWT tokens via `djangorestframework-simplejwt` (1h access / 7d refresh)

### Admin
- Product CRUD (title, description, cost, tax%, image, stock, category)
- Category CRUD (name, logo, description)
- Inline stock update interface (`/products/<id>/stock/`)
- Django Admin panel with custom `UserAdmin`

### Customer
- Home page with category carousel and featured products
- Product listing with category filter tabs and pagination (12/page)
- Product detail page with related items, order form, stock status
- Fuzzy search powered by `pg_trgm` trigram similarity
- Order history with status badges and quick re-order

### API (DRF)
- Full REST API for products, categories, orders
- JWT authentication via `Authorization: Bearer <token>`
- Browsable API at `/api/`

---

## 5. API Design

```
# Auth
POST   /api/auth/register/          → Register new customer
POST   /api/auth/login/             → Get JWT access + refresh tokens
POST   /api/auth/logout/            → Blacklist refresh token
GET    /api/auth/me/                → Get / update current user

# Categories
GET    /api/categories/             → List all categories (public)
POST   /api/categories/             → Create category (admin)
PATCH  /api/categories/<id>/        → Update category (admin)
DELETE /api/categories/<id>/        → Delete category (admin)

# Products
GET    /api/products/               → List products (public)
GET    /api/products/?category=&search=   → Filter by category / keyword
POST   /api/products/               → Create product (admin)
PATCH  /api/products/<id>/          → Update product (admin)
DELETE /api/products/<id>/          → Delete product (admin)
PATCH  /api/products/<id>/stock/    → Update stock only (admin)

# Orders
POST   /api/orders/                 → Place new order
GET    /api/orders/                 → List own orders
GET    /api/orders/<id>/            → Order detail
POST   /api/orders/<id>/reorder/    → Re-order a past order
```

---

## 6. Auth & Roles

| Role | Permissions |
|---|---|
| **Admin** | Full CRUD on products, categories, stock + Django admin panel |
| **Customer** | Browse, search, place orders, view own order history |

| Path | Mechanism | Token Storage |
|---|---|---|
| Django template views | Session cookie | `django_session` table |
| DRF API (`/api/…`) | JWT Bearer token | `outstanding_token` + `blacklisted_token` |

- All admin actions protected with role-check decorator
- Unauthenticated users can browse products and categories (read-only)

---

## 7. Running the Project

### Option A — Docker Compose (Recommended)

```bash
git clone https://github.com/gautamkumar/retail-portal.git
cd retail-portal

cp .env.example .env

docker-compose up --build

# In a separate terminal
docker-compose exec app python manage.py migrate
docker-compose exec app python manage.py createsuperuser
```

### Option B — Local Dev (PostgreSQL via Docker)

```bash
# 1. Start only the database
docker run -d \
  --name retail-portal-db \
  -e POSTGRES_DB=retail_portal \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  postgres:16-alpine

# 2. Enable fuzzy search extension
docker exec retail-portal-db psql -U postgres -d retail_portal \
  -c "CREATE EXTENSION IF NOT EXISTS pg_trgm;"

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env

# 5. Run migrations and start
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000` in your browser.

---

## 8. Environment Variables

Create a `.env` file from `.env.example`:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=retail_portal
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

---

## License

MIT License © 2026 Retail Portal

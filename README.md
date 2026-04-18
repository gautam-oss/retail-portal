# 🛒 Retail Portal — Django Full Stack Project

> A robust, scalable e-commerce platform built with Django 6, Tailwind CSS, pg_trgm fuzzy search, role-based access control, Django REST Framework, and JWT authentication.

---

## 📋 Table of Contents

1. [Project Overview](#1-project-overview)
2. [Repository Structure](#2-repository-structure)
3. [Tech Stack](#3-tech-stack)
4. [Data Models](#4-data-models)
5. [Features](#5-features)
6. [API Design](#6-api-design)
7. [Auth & Roles](#7-auth--roles)
8. [Phase 1 — Project Scaffold](#8-phase-1--project-scaffold)
9. [Phase 2 — Environment Setup & Local Dev](#9-phase-2--environment-setup--local-dev)
10. [Running the Project](#10-running-the-project)
11. [Environment Variables](#11-environment-variables)
12. [Database Diagram](#12-database-diagram)

---

## 1. Project Overview

Retailers need a robust, scalable e-commerce platform that handles:

- **User management** — registration, login, role-based access (Admin / Customer)
- **Product & category management** — full CRUD with image uploads
- **Shopping experience** — KFC-style UI, fuzzy search, pagination, order history, re-ordering
- **API layer** — Django REST Framework with JWT for headless/mobile clients

Built entirely with Django 6 server-side rendered templates + DRF API, PostgreSQL, and Docker for local development.

---

## 2. Repository Structure

```
retail-portal/
├── core/                        # Project settings, root URLs, WSGI
│   ├── settings.py
│   ├── urls.py
│   ├── views.py                 # Home view
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
├── media/                       # User-uploaded files (product/category images)
│
├── .github/
│   └── workflows/
│       └── deploy.yml           # GitHub Actions CI/CD
│
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
| Frontend | Django Templates (HTML + Tailwind CSS via CDN) |
| Database | PostgreSQL 16 |
| Auth | Django Auth (session) + JWT (simplejwt) |
| Fuzzy Search | `pg_trgm` — PostgreSQL trigram extension |
| Static Files | WhiteNoise + Django `staticfiles` |
| Media Files | Django `MEDIA_ROOT` + `MEDIA_URL` |
| CI/CD | GitHub Actions |
| Deployment | Docker + Gunicorn + Nginx |
| Container | Docker + Docker Compose |

---

## 4. Data Models

```python
# accounts/models.py
class User(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=[('admin', 'Admin'), ('customer', 'Customer')],
        default='customer'
    )

# categories/models.py
class Category(models.Model):
    name        = models.CharField(max_length=100, unique=True)
    logo        = models.ImageField(upload_to='categories/', blank=True, null=True)
    description = models.TextField(blank=True)

# products/models.py
class Product(models.Model):
    title        = models.CharField(max_length=200)
    description  = models.TextField(blank=True)
    cost         = models.DecimalField(max_digits=10, decimal_places=2)
    tax_percent  = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    image        = models.ImageField(upload_to='products/', blank=True, null=True)
    stock        = models.IntegerField(default=0)
    category     = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    created_at   = models.DateTimeField(auto_now_add=True)

# orders/models.py
class Order(models.Model):
    STATUS = [('pending','Pending'),('confirmed','Confirmed'),
              ('delivered','Delivered'),('cancelled','Cancelled')]
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status     = models.CharField(max_length=20, choices=STATUS, default='pending')
    total      = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OrderItem(models.Model):
    order    = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
```

---

## 5. Features

### User & Auth
- User sign-up & login (Django session auth + JWT for API)
- Role-Based Access Control: **Admin** and **Customer**
- Protected views with `@login_required` and role checks
- JWT tokens via `djangorestframework-simplejwt` (1h access / 7d refresh)

### Admin
- Product CRUD (title, description, cost, tax%, image, stock, category)
- Category CRUD (name, logo, description)
- Inline stock update interface (`/products/<id>/stock/`)
- Django Admin panel fully configured with custom `UserAdmin`

### Customer
- KFC-style home page — hero banner, category carousel, featured products
- Product listing with category filter tabs + pagination (12/page)
- Product detail page with related items, order form, stock status
- Fuzzy search powered by `pg_trgm` trigram similarity
- Order history with status badges and quick re-order

### API (DRF)
- Full REST API for products, categories, orders
- JWT authentication via `Authorization: Bearer <token>`
- Browsable API at `/api/`

---

## 6. API Design

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

## 7. Auth & Roles

| Role | Permissions |
|---|---|
| **Admin** | Full CRUD on products, categories, stock + Django admin panel |
| **Customer** | Browse, search, place orders, view own order history |

- Session auth for Django template views
- JWT for DRF API endpoints
- All admin actions protected with role-check decorator
- Unauthenticated users can browse products and categories (read-only)

---

## 8. Phase 1 — Project Scaffold

**Status: ✅ Complete**

Everything built from scratch in Phase 1:

| Deliverable | Details |
|---|---|
| Django project | `django-admin startproject core .` |
| 5 apps | `accounts`, `categories`, `products`, `orders`, `search` |
| All models | With migrations generated and verified |
| All views | Template views + DRF API views per app |
| All URL configs | Including DRF router wired in `core/urls.py` |
| All templates | 16 HTML templates — base, navbar, home, per-app CRUD |
| Static files | `static/css/main.css` + `static/js/main.js` |
| Admin | Custom `UserAdmin`, `ProductAdmin`, `CategoryAdmin`, `OrderAdmin` |
| Serializers | Per-app DRF serializers with nested reads |
| `requirements.txt` | All dependencies pinned |
| `.env.example` | Template for environment config |
| `Dockerfile` | Python 3.12 slim + Gunicorn |
| `docker-compose.yml` | `app` + `db` (PostgreSQL) + `nginx` services |
| `nginx.conf` | Reverse proxy + static/media serving |
| GitHub Actions | CI test + Render deploy hook on push to `main` |

**Django system check result:** `0 issues identified`

---

## 9. Phase 2 — Environment Setup & Local Dev

**Status: ✅ Complete**

### What was done

| Step | Result |
|---|---|
| PostgreSQL 16 container started | `docker run ... postgres:16-alpine` on port `5432` |
| `pg_trgm` extension enabled | `CREATE EXTENSION IF NOT EXISTS pg_trgm` |
| `whitenoise`, `Pillow` installed | Via `pip install` |
| `.env` file created | From `.env.example` |
| All migrations applied | 13 migrations across 8 Django apps |
| Superuser created | `admin` / `admin123` |
| Sample data seeded | 5 categories, 12 products |
| Dev server running | `http://127.0.0.1:8000` — all URLs returning 200 |
| Fuzzy search working | `pg_trgm` `TrigramSimilarity` on title + description + category |

### Seeded Data

**Categories:** Burgers · Chicken · Sides · Beverages · Desserts

**Sample Products:**

| Product | Category | Price |
|---|---|---|
| Classic Beef Burger | Burgers | ₹199 |
| Zinger Burger | Burgers | ₹229 |
| Double Patty Burger | Burgers | ₹299 |
| Crispy Chicken Strips | Chicken | ₹179 |
| Bucket Chicken (6pc) | Chicken | ₹499 |
| Spicy Wings (8pc) | Chicken | ₹349 |
| Seasoned Fries | Sides | ₹99 |
| Coleslaw | Sides | ₹49 |
| Corn on the Cob | Sides | ₹79 |
| Pepsi | Beverages | ₹59 |
| Mango Shake | Beverages | ₹129 |
| Choco Sundae | Desserts | ₹99 |

### URL Smoke Test Results (Phase 2)

| URL | Status | Notes |
|---|---|---|
| `http://127.0.0.1:8000/` | ✅ 200 | KFC-style home page |
| `http://127.0.0.1:8000/products/` | ✅ 200 | Product grid with category filters |
| `http://127.0.0.1:8000/categories/` | ✅ 200 | Category listing |
| `http://127.0.0.1:8000/search/?q=burger` | ✅ 200 | Fuzzy search results |
| `http://127.0.0.1:8000/accounts/login/` | ✅ 200 | Login page |
| `http://127.0.0.1:8000/admin/` | ✅ 200 | Django Admin |
| `http://127.0.0.1:8000/api/products/` | ✅ 200 | DRF product list |
| `http://127.0.0.1:8000/api/categories/` | ✅ 200 | DRF category list |

---

## 10. Running the Project

### Option A — Docker Compose (Recommended)

```bash
# Clone the repo
git clone https://github.com/your-username/retail-portal.git
cd retail-portal

# Copy and configure environment
cp .env.example .env

# Start all services (PostgreSQL + Django + Nginx)
docker-compose up --build

# In a separate terminal — run migrations and create superuser
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

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your values

# 5. Run migrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Seed sample data (optional)
python manage.py shell < scripts/seed.py   # if seed script exists

# 8. Start dev server
python manage.py runserver
```

Open `http://127.0.0.1:8000` in your browser.

### Default Credentials (dev only)

| Username | Password | Role |
|---|---|---|
| `admin` | `admin123` | Admin |

---

## 11. Environment Variables

Create a `.env` file in the project root based on `.env.example`:

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

### settings.py — Static & Media Config

```python
STATIC_URL  = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL   = '/media/'
MEDIA_ROOT  = BASE_DIR / 'media'
```

WhiteNoise serves static files in production without Nginx for simple setups.

---

## 12. Database Diagram

```
                                   ┌──────────────────────────────────┐
                                   │            AUTH_USER             │
                                   │         (accounts app)           │
                                   ├──────────────────────────────────┤
                                   │ id          (PK, serial)         │
                                   │ username    (varchar, unique)     │
                                   │ email       (varchar, unique)     │
                                   │ password    (varchar, hashed)     │
                                   │ first_name  (varchar)            │
                                   │ last_name   (varchar)            │
                                   │ role        (varchar)  ← custom  │
                                   │ is_active   (bool)               │
                                   │ is_staff    (bool)               │
                                   │ is_superuser(bool)               │
                                   │ date_joined (timestamptz)        │
                                   │ last_login  (timestamptz)        │
                                   └───┬──────────────────────────────┘
                                       │ 1
              ┌────────────────────────┼─────────────────────────────────────┐
              │ many                   │ many                                 │ 1
              ▼                        ▼                                      │
┌─────────────────────┐   ┌────────────────────────────┐                     │
│        ORDER        │   │      OUTSTANDING_TOKEN      │                     │
│    (orders app)     │   │  (simplejwt — refresh JWT)  │                     │
├─────────────────────┤   ├────────────────────────────┤                     │
│ id         (PK)     │   │ id         (PK)             │                     │
│ user_id    (FK) ────┼───│ user_id    (FK)             │                     │
│ status     (varchar)│   │ jti        (varchar, unique) │                    │
│ total      (decimal)│   │ token      (text)           │                     │
│ created_at (ts)     │   │ created_at (timestamptz)    │                     │
│ updated_at (ts)     │   │ expires_at (timestamptz)    │                     │
└──────────┬──────────┘   └────────────┬───────────────┘                     │
           │ 1                         │ 1                                    │
           │ many                      │ 0..1                                 │
           ▼                           ▼                                      │
┌─────────────────────┐   ┌────────────────────────────┐                     │
│      ORDER_ITEM     │   │      BLACKLISTED_TOKEN      │                     │
│    (orders app)     │   │  (simplejwt — after logout) │                     │
├─────────────────────┤   ├────────────────────────────┤                     │
│ id         (PK)     │   │ id                  (PK)   │                     │
│ order_id   (FK)     │   │ token_id            (FK) ──┘                     │
│ product_id (FK) ─┐  │   │ blacklisted_at (timestamptz)│                    │
│ quantity         │  │   └────────────────────────────┘                     │
│ subtotal(decimal)│  │                                                       │
└──────────────────┘  │                                                       │
                       │ many                                                  │
                       │                                                       │
                       │     ┌─────────────────────────┐                      │
                       │     │        CATEGORY          │                      │
                       │     │    (categories app)      │                      │
                       │     ├─────────────────────────┤                      │
                       │     │ id          (PK)         │                      │
                       │     │ name        (varchar)    │                      │
                       │     │ logo        (varchar)    │                      │
                       │     │ description (text)       │                      │
                       │     └────────────┬────────────┘                      │
                       │                  │ 1                                  │
                       │                  │ many                               │
                       │                  ▼                                    │
                       │     ┌─────────────────────────┐                      │
                       └─────│         PRODUCT          │                      │
                        1    │     (products app)       │                      │
                             ├─────────────────────────┤                      │
                             │ id           (PK)        │                      │
                             │ title        (varchar)   │                      │
                             │ description  (text)      │                      │
                             │ cost         (decimal)   │                      │
                             │ tax_percent  (decimal)   │                      │
                             │ image        (varchar)   │                      │
                             │ stock        (int)       │                      │
                             │ category_id  (FK)        │                      │
                             │ is_available (bool)      │                      │
                             │ created_at   (ts)        │                      │
                             └─────────────────────────┘                      │

┌──────────────────────────────────────────────────┐                          │
│              DJANGO_SESSION                       │                          │
│         (session auth — template views)           │                          │
├──────────────────────────────────────────────────┤                          │
│ session_key  (varchar PK)                        │                          │
│ session_data (text — pickled + base64)           │  ← holds user_id ────────┘
│ expire_date  (timestamptz, indexed)              │
└──────────────────────────────────────────────────┘
```

### Auth Flow — Two Parallel Systems

| Path | Mechanism | Token Storage |
|---|---|---|
| Django template views | Session cookie | `django_session` table |
| DRF API (`/api/…`) | JWT Bearer token | `outstanding_token` + `blacklisted_token` |

### All Relationships

| From | To | Type | Notes |
|---|---|---|---|
| `auth_user` → `order` | One → Many | user places many orders |
| `auth_user` → `outstanding_token` | One → Many | one user, many issued JWTs |
| `outstanding_token` → `blacklisted_token` | One → 0..1 | token blacklisted on logout |
| `category` → `product` | One → Many | product belongs to one category |
| `order` → `order_item` | One → Many | order has multiple line items |
| `product` → `order_item` | One → Many | product appears in many order items |
| `auth_user` → `django_session` | One → Many | one user, many browser sessions |

---

## 🚀 Phase 3 — Render Deploy

**Status: ✅ Complete**

### What was done

| Step | Result |
|---|---|
| `render.yaml` created | Defines `retail-portal` web service + `retail-portal-db` managed PostgreSQL (free plan) |
| `dj-database-url` added | `requirements.txt` — parses Render's `DATABASE_URL` with `conn_max_age=600` |
| `settings.py` updated | `DATABASE_URL` takes precedence over individual `DB_*` vars; `RENDER_EXTERNAL_HOSTNAME` auto-appended to `ALLOWED_HOSTS` |
| `.env.example` updated | Added production section documenting Render env vars |
| `collectstatic` on deploy | Already in `buildCommand` inside `render.yaml` |
| Migrations on deploy | `python manage.py migrate` runs in `buildCommand` before server starts |
| GitHub Actions deploy job | Triggers Render deploy hook via `RENDER_DEPLOY_HOOK` secret on push to `main` |

### Deploy Steps (one-time manual setup)

1. Push this repo to GitHub
2. Go to [render.com](https://render.com) → **New → Blueprint** → connect your repo
3. Render reads `render.yaml` and creates the web service + PostgreSQL database automatically
4. In the web service **Environment** tab, verify these are set (render.yaml injects `DATABASE_URL` automatically):
   - `SECRET_KEY` — auto-generated ✅
   - `DEBUG` → `False` ✅
   - `ALLOWED_HOSTS` → `.onrender.com` ✅
5. Copy the **Deploy Hook URL** from the Render dashboard → add as `RENDER_DEPLOY_HOOK` secret in GitHub repo settings
6. Every push to `main` now runs CI tests → triggers Render deploy on success

### Environment Variables (Production)

| Variable | Source | Value |
|---|---|---|
| `SECRET_KEY` | render.yaml `generateValue` | Auto-generated by Render |
| `DEBUG` | render.yaml | `False` |
| `ALLOWED_HOSTS` | render.yaml | `.onrender.com` |
| `DATABASE_URL` | render.yaml `fromDatabase` | Auto-injected from linked PostgreSQL |
| `RENDER_EXTERNAL_HOSTNAME` | Render platform | Auto-set — appended to `ALLOWED_HOSTS` in `settings.py` |

---

## 📄 License

MIT License © 2025 Retail Portal

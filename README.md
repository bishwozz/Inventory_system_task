## Project Structure Overview

inventory_system_task/
├── app/
│   ├── config/
│   │   └── settings.py        # Pydantic settings & env var loader
│   ├── controllers/
│   │   ├── auth.py            # login, JWT token endpoint
│   │   ├── users.py           # user CRUD (RBAC)
│   │   ├── products.py        # product endpoints
│   │   ├── inventory.py       # stock add/remove & queries
│   │   └── alerts.py          # low-stock & expiry alerts
│   ├── database/
│   │   ├── base.py            # declarative Base import
│   │   ├── session.py         # AsyncSession maker
│   │   └── migrations/        # Alembic migration scripts
│   ├── models/
│   │   ├── user.py            # User table
│   │   ├── product.py         # Product table
│   │   ├── inventory_entry.py # InventoryEntry table
│   │   ├── pricing_rule.py    # PricingRule table
│   │   └── alert.py           # Alert table
│   ├── schemas/
│   │   ├── user.py            # Pydantic models for User
│   │   ├── product.py         # schemas for Product
│   │   ├── inventory.py       # schemas for InventoryEntry
│   │   └── alert.py           # schemas for Alert
│   ├── tasks/
│   │   └── celery.py          # Celery app & periodic task setup
│   ├── utils/
│   │   ├── cache.py           # Redis caching helpers
│   │   └── rate_limit.py      # rate‑limiting decorators
│   └── main.py                # FastAPI app instantiation, router includes
├── Dockerfile                 # Build Python/FastAPI container
├── requirements.txt           # Pinned dependencies
├── docker-compose.yml         # Orchestrate services (Postgres, Redis, app, Celery)
└── README.md                  # Setup & usage documentation

### 🧪 Lightweight Inventory System (FastAPI + PostgreSQL + Redis + Celery)

A lightweight inventory system with support for expiration tracking, dynamic pricing, low stock alerts, and rate-limited endpoints.

---

## 📦 Tech Stack

- FastAPI 🚀
- PostgreSQL 🐘
- Redis ⚡
- Celery 🎯
- Docker 🐳

---

## ⚙️ Setup Instructions

### 1. Clone the repo

```bash
git clone <your-repo-url>
cd inventory-system
```

## 2. Create .env file

env
Copy
Edit
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/inventory_db
REDIS_URL=redis://redis:6379

## 3. Run using Docker Compose

bash
Copy
Edit
docker-compose build
docker-compose up -d

## 🛠 Sample Endpoints

✅ Add Inventory
http
Copy
Edit
POST /api/v1/inventory/
Body:

json
Copy
Edit
{
"product_id": 1,
"quantity": 5,
"expiration_date": "2025-05-01T00:00:00"
}

## 🔄 Trigger Celery Task (Manual)

bash
Copy
Edit
docker exec -it celery_worker celery -A app.worker.celery_app call app.tasks.inventory_tasks.

## 🔁 Pricing Rule Logic

If inventory is expiring in ≤3 days → 20% price discount

Products with total quantity < 5 → trigger alert

## 🧱 System Overview

                     ┌────────────┐
                     │   Client   │
                     └─────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  FastAPI    │
                    └──────┬──────┘
                           │
          ┌────────┬───────┼─────────────┐
          │        │       │             │
          ▼        ▼       ▼             ▼
      PostgreSQL  Redis   Celery       Docker
    (Inventory DB) (Cache) (Worker) (Infra)




seeder

docker compose exec web python3 -m app.seed.seed_users

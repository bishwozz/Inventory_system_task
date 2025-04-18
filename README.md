## Project Structure Overview

inventory_system_task/ # Root folder of the project
├── app/ # Your actual FastAPI application code lives here
│ ├── api/ # All your API route definitions (like /users, /products)
│ │ └── v1/ # Versioned API
│ │ └── endpoints/
│ ├── core/ # Core configs like settings, JWT, and security logic
│ ├── crud/ # CRUD operations that talk to the DB
│ ├── db/ # DB models and DB session setup
│ ├── schemas/ # Pydantic schemas for request/response validation
│ ├── services/ # Business logic like pricing/alerting
│ ├── tasks/ # Celery background task functions
│ ├── cache/ # Redis caching, rate-limiting logic
│ ├── main.py # Entry point for FastAPI app
│ └── celery_worker.py # Entry point for Celery
├── docker-compose.yml # Run all services with one command
├── Dockerfile # Builds your FastAPI app container
├── .env # Environment variables (database/redis URLs)
├── requirements.txt # Python packages needed
├── README.md # Project documentation
└── seed/ # Initial SQL data for demo

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

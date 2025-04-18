## Project Structure Overview

inventory_system_task/          # Root folder of the project
├── app/                        # Your actual FastAPI application code lives here
│   ├── api/                    # All your API route definitions (like /users, /products)
│   │   └── v1/                 # Versioned API
│   │       └── endpoints/
│   ├── core/                   # Core configs like settings, JWT, and security logic
│   ├── crud/                   # CRUD operations that talk to the DB
│   ├── db/                     # DB models and DB session setup
│   ├── schemas/                # Pydantic schemas for request/response validation
│   ├── services/               # Business logic like pricing/alerting
│   ├── tasks/                  # Celery background task functions
│   ├── cache/                  # Redis caching, rate-limiting logic
│   ├── main.py                 # Entry point for FastAPI app
│   └── celery_worker.py        # Entry point for Celery
├── docker-compose.yml          # Run all services with one command
├── Dockerfile                  # Builds your FastAPI app container
├── .env                        # Environment variables (database/redis URLs)
├── requirements.txt            # Python packages needed
├── README.md                   # Project documentation
└── seed/                       # Initial SQL data for demo
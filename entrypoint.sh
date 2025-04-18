#!/bin/bash

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
while ! nc -z db 5432; do
  sleep 0.5
done
echo "✅ PostgreSQL is ready!"

# Auto-create tables
echo "📦 Creating tables..."
python -c "from app.database.database import Base, engine; Base.metadata.create_all(bind=engine)"

# Seed data
echo "🌱 Seeding the database..."
python /app/seed/seed_data.py

# Start the app
echo "🚀 Starting FastAPI app..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

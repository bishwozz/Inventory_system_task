# Inventory System Documentation

## Setup Instructions (Docker)

To get the project up and running with Docker, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. **Build and run the Docker containers:**
   Ensure Docker is installed on your machine. Then, run the following command to build and start the containers:

   ```bash
   docker-compose up --build
   ```

3. **Access the app:**
   Once the containers are up, you can access the FastAPI app via [http://localhost:8000](http://localhost:8000).

4. **Access the Swagger API docs:**
   FastAPI automatically generates API documentation using Swagger. Access it by going to:

   ```bash
   http://localhost:8000/docs
   ```

5. **Database setup (Optional for first run):**
   The Docker Compose setup will automatically create and migrate the database. However, if you want to manually create the database schema, you can use the following command:
   ```bash
   docker-compose exec app python -c 'from app.db.base import Base, engine; Base.metadata.create_all(bind=engine)'
   ```

---

## Sample API Usage

Here are some sample API requests to interact with your inventory system:

### 1. **User Registration**

**POST** `/api/v1/register`

Example Request Body:

```json
{
  "email": "user@example.com",
  "password": "password123",
  "role": "user"
}
```

### 2. **User Login**

**POST** `/api/v1/login`

Example Request Body:

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response**:

```json
{
  "access_token": "jwt_token_here",
  "token_type": "bearer"
}
```

---

### 3. **Create Product (Admin only)**

**POST** `/api/v1/products/`

Example Request Body:

```json
{
  "name": "Product A",
  "description": "A test product",
  "price": 100.0,
  "expiration_date": "2025-12-31T00:00:00"
}
```

---

### 4. **Get Product by ID**

**GET** `/api/v1/products/{product_id}`

---

### 5. **Update Product (Admin only)**

**PUT** `/api/v1/products/{product_id}/`

Example Request Body:

```json
{
  "price": 120.0
}
```

---

### 6. **Delete Product (Admin only)**

**DELETE** `/api/v1/products/{product_id}`

---

### 7. **List Products (With Pagination)**

**GET** `/api/v1/products/`

Example Query Parameters:

```bash
/products?expiring_in=7&page=1&limit=10
```

---

## System Overview Diagram

Here’s a simple diagram to represent the overall system architecture:

```
+------------------+      +------------------+      +------------------+
|  FastAPI (App)   | <---> |   PostgreSQL     | <---> |    Redis Cache   |
+------------------+      +------------------+      +------------------+
        |                        |                         |
   +-------------+         +-------------+          +------------------+
   | Celery Worker|         | Celery Beat |          |  API Requests   |
   +-------------+         +-------------+          +------------------+
```

---

## Description of Pricing Rule Logic

The pricing rule is applied based on the expiration proximity of the product. For example:

- If a product is nearing its expiration date (within the next 15 days), the price is adjusted by a set percentage (e.g., 10% off).
- This helps clear out near-expiry items by making them more attractive to customers.

### Example:

If a product has an original price of $100 and is set to expire in 10 days, applying a 10% discount would result in a new price of $90.

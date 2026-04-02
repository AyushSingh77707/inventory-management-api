# Inventory Management API

A backend REST API for managing products, orders, and users with 
real-time stock tracking and low-stock alerts.

Built with **FastAPI · PostgreSQL · Redis · Celery · JWT Auth**

---

 ## Features

- Product CRUD — add, update, delete, list products
- Order CRUD — place and manage orders
- Stock Tracking — real-time inventory levels
- Low Stock Alerts — automatic notifications via Celery
- RBAC — role-based access control (admin/user)
- JWT Authentication — secure token-based auth

---

## Tech Stack

| Layer        | Technology              |
|--------------|-------------------------|
| Framework    | FastAPI                 |
| Database     | PostgreSQL + SQLAlchemy |
| Validation   | Pydantic                |
| Auth         | JWT (OAuth2)            |
| Cache/Queue  | Redis                   |
| Background   | Celery                  |

---

## Getting Started

### Prerequisites
- Python 3.10+
- PostgreSQL
- Redis

### Installation
```bash
git clone https://github.com/AyushSingh77707/inventory-management-api
cd inventory-management-api
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file:
```
DATABASE_URL=postgresql://user:password@localhost/inventory_db
SECRET_KEY=your_secret_key
REDIS_URL=redis://localhost:6379
```

### Run
```bash
uvicorn app.main:app --reload
```

API docs available at: `http://localhost:8000/docs`

---

## API Overview

| Method | Endpoint           | Description         |
|--------|--------------------|---------------------|
| POST   | /auth/register     | Register user       |
| POST   | /auth/login        | Login & get token   |
| GET    | /products          | List all products   |
| POST   | /products          | Add product         |
| PUT    | /products/{id}     | Update product      |
| DELETE | /products/{id}     | Delete product      |
| GET    | /orders            | List orders         |
| POST   | /orders            | Place order         |
| GET    | /stock/alerts      | Get low stock items |

---

## Author

**Ayush Singh** — [LinkedIn](https://www.linkedin.com/in/ayush-singh-114a5b307/) · [GitHub](https://github.com/AyushSingh77707)

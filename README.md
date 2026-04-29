# Matz Auto Repair API

API for managing mechanics, customers, service tickets, and inventory.

---

## 🌐 Live API

Base URL:
https://matz-auto-repair.onrender.com

---

## 📄 API Documentation

Swagger UI:
https://matz-auto-repair.onrender.com/api/docs/

---

## 📌 Endpoints

### Mechanics
GET /mechanics/
POST /mechanics/

### Customers
GET /customers/
POST /customers/

### Service Tickets
GET /service-tickets/
POST /service-tickets/

### Inventory
GET /inventory/
POST /inventory/

---

## ⚙️ Tech Stack

- Flask
- SQLAlchemy
- Marshmallow
- Swagger (Flask-Swagger)
- PostgreSQL (Render)
- Gunicorn

---

## 🧪 Testing

Run tests with:

```bash
python -m unittest discover tests
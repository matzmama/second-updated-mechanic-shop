# Mechanic Shop API

A Flask-based REST API for managing a mechanic shop. This API handles customers, mechanics, service tickets, and inventory with token-based authentication, rate limiting, caching, documentation, and testing.

---

## Features

* **Customer Management** — Create, read, update, and delete customers with pagination
* **Mechanic Management** — Create and manage mechanics, ordered by most tickets worked
* **Service Tickets** — Create and manage service tickets linked to customers and mechanics
* **Inventory** — Track parts and assign them to service tickets
* **Token Authentication** — Role-based JWT tokens for customers and mechanics
* **Rate Limiting** — Protection against abuse using Flask-Limiter
* **Caching** — Improved performance using Flask-Caching
* **API Documentation** — Fully documented endpoints using Swagger
* **Unit Testing** — Automated tests for all endpoints using unittest

---

## Tech Stack

* Python 3.12
* Flask
* SQLAlchemy
* Flask-Marshmallow
* Flask-Limiter
* Flask-Caching
* python-jose (JWT)
* SQLite

---

## Project Structure

```
Mechanic_Final_Project/
├── app.py
├── config.py
├── application/
│   ├── __init__.py
│   ├── extensions.py
│   ├── models.py
│   └── blueprints/
│       ├── customer/
│       │   ├── __init__.py
│       │   └── routes.py
│       ├── mechanic/
│       │   ├── __init__.py
│       │   └── routes.py
│       ├── service_ticket/
│       │   ├── __init__.py
│       │   └── routes.py
│       ├── inventory/
│       │   ├── __init__.py
│       │   └── routes.py
│       └── utils/
│           ├── __init__.py
│           └── util.py
├── tests/
│   ├── test_customers.py
│   ├── test_mechanics.py
│   ├── test_service_tickets.py
│   └── test_inventory.py
└── instance/
    └── mechanics.db
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/matzmama/Mechanic_Final_Project.git
cd Mechanic_Final_Project
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

### 3. Install dependencies

```bash
pip install flask flask-sqlalchemy flask-marshmallow marshmallow-sqlalchemy flask-limiter flask-caching python-jose
```

### 4. Run the application

```bash
python app.py
```

The server will start at `http://127.0.0.1:5000`

---

## API Documentation (Swagger)

This API includes full documentation using Swagger UI.

### Access Swagger:

```
http://127.0.0.1:5000/api/docs
```

### Documentation Includes:

* Endpoint paths and HTTP methods
* Tags for grouping routes
* Summaries and detailed descriptions
* Request body schemas (POST/PUT)
* Response schemas for all endpoints
* Example request and response data
* Defined models for:

  * Customer
  * Mechanic
  * ServiceTicket
  * Inventory

---

## API Endpoints

### Customers — `/customers`

| Method | Endpoint           | Auth           | Description         |
| ------ | ------------------ | -------------- | ------------------- |
| POST   | `/customers/`      | None           | Create a customer   |
| GET    | `/customers/`      | None           | Get all customers   |
| POST   | `/customers/login` | None           | Login and get token |
| PUT    | `/customers/<id>`  | Customer Token | Update customer     |
| DELETE | `/customers/<id>`  | Customer Token | Delete customer     |

---

### Mechanics — `/mechanics`

| Method | Endpoint               | Auth           | Description                  |
| ------ | ---------------------- | -------------- | ---------------------------- |
| POST   | `/mechanics/`          | None           | Create a mechanic            |
| GET    | `/mechanics/`          | None           | Get all mechanics            |
| POST   | `/mechanics/login`     | None           | Login and get mechanic token |
| GET    | `/mechanics/protected` | Mechanic Token | Protected route              |

---

### Service Tickets — `/service-tickets`

| Method | Endpoint                         | Auth           | Description          |
| ------ | -------------------------------- | -------------- | -------------------- |
| POST   | `/service-tickets/`              | Customer Token | Create a ticket      |
| GET    | `/service-tickets/`              | Mechanic Token | Get all tickets      |
| GET    | `/service-tickets/my-tickets`    | Customer Token | Get customer tickets |
| PUT    | `/service-tickets/<id>/assign`   | Mechanic Token | Assign mechanic      |
| PUT    | `/service-tickets/<id>/edit`     | Mechanic Token | Modify mechanics     |
| PUT    | `/service-tickets/<id>/add-part` | Mechanic Token | Add part             |

---

### Inventory — `/inventory`

| Method | Endpoint          | Auth           | Description   |
| ------ | ----------------- | -------------- | ------------- |
| POST   | `/inventory/`     | Mechanic Token | Create a part |
| GET    | `/inventory/`     | None           | Get all parts |
| GET    | `/inventory/<id>` | None           | Get one part  |
| PUT    | `/inventory/<id>` | Mechanic Token | Update part   |
| DELETE | `/inventory/<id>` | Mechanic Token | Delete part   |

---

## Authentication

This API uses JWT Bearer tokens.

### Customer Login

```
POST /customers/login
{
  "email": "test@test.com",
  "password": "password123"
}
```

### Mechanic Login

```
POST /mechanics/login
{
  "id": 1
}
```

### Using Tokens

```
Authorization: Bearer <your_token_here>
```

---

## Unit Testing

This project includes full unit testing using Python’s `unittest`.

### Test Coverage Includes:

* GET requests for all resources
* POST requests for all resources
* Negative test cases (invalid input)
* Protected route testing (401 responses)

### Run Tests

```bash
python -m unittest discover tests
```

### Testing Approach

* Each blueprint has its own test file
* Database is reset before each test:

```python
db.drop_all()
db.create_all()
```

* Tests follow Test-Driven Development principles:

  * Red → tests fail initially
  * Green → code written to pass tests
  * Refactor → improved structure and validation

---

## Example Usage

### Create a customer

```
POST /customers/
{
  "name": "Jane Doe",
  "email": "jane@test.com",
  "password": "password123"
}
```

### Create a service ticket

```
POST /service-tickets/
Authorization: Bearer <customer_token>
{
  "description": "Oil change needed"
}
```

### Add a part

```
PUT /service-tickets/1/add-part
Authorization: Bearer <mechanic_token>
{
  "part_id": 1
}
```

---

## GitHub Repository

https://github.com/matzmama/Updated-Mechanic-Shop.git

---

## License

This project was built as part of a software engineering course assignment.

# Order Management API (Flask)

## Features
- JWT Authentication
- Product CRUD
- Order Processing
- Pricing Logic (Discounts)

## Setup
pip install flask flask_sqlalchemy flask_jwt_extended
python app.py

## Endpoints

### Register
POST /register
{
  "username": "admin",
  "password": "admin"
}

### Login
POST /login

### Create Product
POST /products

### Get Products
GET /products

### Create Order
POST /orders

## Sample Order Request
{
  "products": [
    {"product_id": 1, "quantity": 2},
    {"product_id": 2, "quantity": 1}
  ]
}

## Pricing Logic
- 10% discount if total > 1000

## CV Points
- Developed REST API using Flask
- Implemented JWT Authentication
- Used SQLAlchemy ORM
- Designed pricing logic
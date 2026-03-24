# =========================
# Flask Order Management API
# =========================


from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_required, get_jwt_identity
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
app.config['JWT_SECRET_KEY'] = 'super-secret'

db = SQLAlchemy(app)
jwt = JWTManager(app)

# =========================
# Models
# =========================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    total_price = db.Column(db.Float)

# =========================
# Auth Routes
# =========================
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    user = User(username=data['username'], password=data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify(msg="User created")

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username'], password=data['password']).first()
    if not user:
        return jsonify(msg="Invalid credentials"), 401
    token = create_access_token(identity=str(user.id))
    return jsonify(access_token=token)

# =========================
# Product CRUD
# =========================
@app.route('/products', methods=['POST'])
@jwt_required()
def create_product():
    data = request.json
    product = Product(name=data['name'], price=data['price'])
    db.session.add(product)
    db.session.commit()
    return jsonify(msg="Product created")

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([
        {"id": p.id, "name": p.name, "price": p.price} for p in products
    ])

# =========================
# Order Creation
# =========================
@app.route('/orders', methods=['POST'])
@jwt_required()
def create_order():
    user_id = int(get_jwt_identity())
    data = request.json

    total = 0
    for item in data['products']:
        product = Product.query.get(item['product_id'])
        total += product.price * item['quantity']

    # Pricing logic (10% discount if > 1000)
    if total > 1000:
        total *= 0.9

    order = Order(user_id=user_id, total_price=total)
    db.session.add(order)
    db.session.commit()

    return jsonify({"msg": "Order created", "total": total})

# =========================
# Init DB + Dummy Data
# =========================
def create_tables():
    db.create_all()

    if not User.query.first():
        user = User(username="admin", password="admin")
        db.session.add(user)

        p1 = Product(name="Laptop", price=700)
        p2 = Product(name="Phone", price=500)
        p3 = Product(name="Headphones", price=100)

        db.session.add_all([p1, p2, p3])
        db.session.commit()

# =========================
# Run
# =========================
if __name__ == '__main__':
    with app.app_context():
        create_tables()
    app.run(debug=True)

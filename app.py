from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import stripe

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Replace with a secret key for session management
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/ecommerce'  # Replace with your database URI

# Initialize Flask extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
stripe.api_key = 'your_stripe_secret_key_here'  # Replace with your Stripe secret key

# Define the User model for user authentication
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    
# Define the Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)

# Define the CartItem model
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)

    user = db.relationship('User', backref='cart_items')
    product = db.relationship('Product', backref='cart_items')

# Define the Order model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    date_ordered = db.Column(db.DateTime, nullable=False)

    user = db.relationship('User', backref='orders')

# Configure Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already registered.', 'error')
            return redirect(url_for('register'))

        new_user = User(username=username, email=email, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash('Invalid email or password.', 'error')
            return redirect(url_for('login'))

        login_user(user)
        flash('Logged in successfully.', 'success')
        return redirect(url_for('home'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('home'))


@app.route('/')
def home():
    # Implement logic to fetch product information from the database and display it on the home page
    return render_template('layouts/main.html', products=[])

# Implement routes for product listing, product details, cart, and checkout
# You can define functions to handle the interactions with the database and render the appropriate templates


@app.route('/add_to_cart/<int:product_id>')
@login_required
def add_to_cart(product_id):
    # Implement logic to add items to the cart and store cart items in the database
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:product_id>')
@login_required
def remove_from_cart(product_id):
    # Implement logic to remove items from the cart and update cart items in the database
    return redirect(url_for('cart'))

@app.route('/cart')
@login_required
def cart():
    # Implement logic to fetch cart items from the database and display them in the cart page
    return render_template('cart.html', cart_items=[])

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# ... (other code)

# Configure Flask-Login
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


from markupsafe import escape

@app.route('/product/<int:product_id>')
def product_details(product_id):
    product = Product.query.get_or_404(product_id)
    # Escaping user-generated content before rendering it in the template
    return render_template('product_details.html', product=escape(product))

@app.route('/search')
def search():
    search_term = request.args.get('query')
    # Use parameterized queries with SQLAlchemy to prevent SQL injection
    products = Product.query.filter(Product.name.ilike(f"%{search_term}%")).all()
    # ...
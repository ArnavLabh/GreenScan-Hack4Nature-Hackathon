from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User, Scan
import json
from flask import jsonify
import os
from datetime import datetime

main = Blueprint('main', __name__)

# Load products data
def load_products():
    try:
        # Try to load from the data directory first
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'products.json')
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return json.load(f)
        
        # If not found in data directory, try the root directory
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'products.json')
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return json.load(f)
                
        print("Warning: products.json not found")
        return []
    except Exception as e:
        print(f"Error loading products: {e}")
        return []

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/scan')
@login_required
def scan():
    return render_template('scan.html')

@main.route('/search')
@login_required
def search():
    query = request.args.get('query', '').strip()
    category = request.args.get('category')
    
    products = load_products()
    categories = list(set(p['category'] for p in products))
    
    if query:
        products = [p for p in products if query.lower() in p['name'].lower()]
    
    if category:
        products = [p for p in products if p['category'] == category]
    
    return render_template('search.html', 
                         products=products,
                         categories=categories,
                         query=query,
                         category=category)

@main.route('/result', methods=['GET', 'POST'])
@login_required
def result():
    try:
        if request.method == 'POST':
            barcode = request.form.get('barcode')
        else:
            barcode = request.args.get('barcode')
            
        if not barcode:
            flash('No barcode provided', 'danger')
            return redirect(url_for('main.scan'))
        
        products = load_products()
        product = next((p for p in products if str(p['barcode']) == str(barcode)), None)
        
        if not product:
            flash('Product not found', 'warning')
            return redirect(url_for('main.scan'))
        
        # Record the scan
        try:
            scan = Scan(
                user_id=current_user.id,
                product_name=product['name'],
                barcode=barcode,
                recyclable=product['category'] in ['Glass', 'Paper']  # Consider glass and paper as recyclable
            )
            db.session.add(scan)
            db.session.commit()
        except Exception as e:
            # Log the error but continue to show the result
            print(f"Error recording scan: {e}")
        
        return render_template('result.html', product=product)
    except Exception as e:
        print(f"Error in result route: {e}")
        flash('An error occurred while processing your request', 'danger')
        return redirect(url_for('main.scan'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main.index'))
        flash('Invalid email or password', 'danger')
    return render_template('login.html')

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    try:
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')
            
            print(f"Signup attempt - Name: {name}, Email: {email}")  # Log signup attempt
            
            if not all([name, email, password]):
                print("Missing required fields")  # Log missing fields
                flash('All fields are required', 'danger')
                return redirect(url_for('main.signup'))
            
            try:
                # Check if user exists
                existing_user = User.query.filter_by(email=email).first()
                if existing_user:
                    print(f"Email already registered: {email}")  # Log duplicate email
                    flash('Email already registered', 'danger')
                    return redirect(url_for('main.signup'))
                
                # Create new user
                user = User(name=name, email=email)
                user.set_password(password)
                
                print("Attempting to add user to database")  # Log database operation
                db.session.add(user)
                db.session.commit()
                print("User successfully added to database")  # Log success
                
                login_user(user)
                flash('Account created successfully!', 'success')
                return redirect(url_for('main.index'))
            except Exception as e:
                db.session.rollback()
                print(f"Database error during signup: {str(e)}")  # Log database error
                print(f"Error type: {type(e)}")  # Log error type
                flash('An error occurred during signup. Please try again.', 'danger')
                return redirect(url_for('main.signup'))
                
        return render_template('signup.html')
    except Exception as e:
        print(f"Unexpected error in signup route: {str(e)}")  # Log unexpected error
        print(f"Error type: {type(e)}")  # Log error type
        flash('An unexpected error occurred. Please try again.', 'danger')
        return redirect(url_for('main.signup'))

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('main.index'))

@main.route('/profile')
@login_required
def profile():
    scans = Scan.query.filter_by(user_id=current_user.id).order_by(Scan.timestamp.desc()).all()
    scan_count = len(scans)
    recyclable_count = sum(1 for scan in scans if scan.recyclable)
    non_recyclable_count = scan_count - recyclable_count
    
    return render_template('profile.html', 
                         scans=scans,
                         scan_count=scan_count,
                         recyclable_count=recyclable_count,
                         non_recyclable_count=non_recyclable_count)

@main.route('/settings')
@login_required
def settings():
    return render_template('settings.html')

@main.route('/categories')
def get_categories():
    products = load_products()
    categories = list(set(p['category'] for p in products))
    return jsonify(categories)

@main.route('/api/scan', methods=['POST'])
def api_scan():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    image = request.files['image']
    if image.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Here you would implement the barcode scanning logic
    # For now, we'll return a mock response
    return jsonify({
        'success': True,
        'barcode': '8906017290064'  # Example barcode
    })

@main.route('/api/stats')
@login_required
def get_stats():
    scans = Scan.query.filter_by(user_id=current_user.id).order_by(Scan.timestamp.desc()).all()
    total_scans = len(scans)
    recyclable_count = sum(1 for scan in scans if scan.recyclable)
    
    recent_activity = []
    for scan in scans[:5]:
        recent_activity.append({
            'product_name': scan.product_name,
            'recyclable': scan.recyclable,
            'time': scan.timestamp.strftime('%Y-%m-%d %H:%M')
        })
    
    return jsonify({
        'total_scans': total_scans,
        'recycling_impact': recyclable_count,
        'recent_activity': recent_activity
    })

@main.route('/image-recognition')
@login_required
def image_recognition():
    return render_template('image_recognition.html')
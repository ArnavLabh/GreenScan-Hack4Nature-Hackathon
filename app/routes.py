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
        with open('data/products.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading products: {e}")
        return []

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/scan')
def scan():
    return render_template('scan.html')

@main.route('/search')
def search():
    query = request.args.get('q', '').lower()
    products = load_products()
    if query:
        products = [p for p in products if query in p['name'].lower()]
    return render_template('search.html', products=products, query=query)

@main.route('/result', methods=['POST'])
def result():
    barcode = request.form.get('barcode')
    if not barcode:
        flash('No barcode provided', 'danger')
        return redirect(url_for('main.scan'))
    
    products = load_products()
    product = next((p for p in products if str(p['barcode']) == str(barcode)), None)
    
    if not product:
        flash('Product not found', 'warning')
        return redirect(url_for('main.scan'))
    
    if current_user.is_authenticated:
        # Record the scan
        scan = Scan(
            user_id=current_user.id,
            product_name=product['name'],
            barcode=barcode,
            recyclable=product['category'] in ['Glass', 'Paper']  # Consider glass and paper as recyclable
        )
        db.session.add(scan)
        db.session.commit()
    
    return render_template('result.html', product=product)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember') == 'on'
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.index'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login.html')

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('signup.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return render_template('signup.html')
        
        user = User(name=name, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        return redirect(url_for('main.index'))
    
    return render_template('signup.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/profile')
@login_required
def profile():
    user_scans = Scan.query.filter_by(user_id=current_user.id).order_by(Scan.scanned_at.desc()).all()
    return render_template('profile.html', user=current_user, scans=user_scans)

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
    # Get user's scan history
    scans = Scan.query.filter_by(user_id=current_user.id).order_by(Scan.scanned_at.desc()).all()
    
    # Calculate statistics
    total_scans = len(scans)
    recyclable_count = sum(1 for scan in scans if scan.recyclable)
    recycling_impact = round((recyclable_count / total_scans * 100) if total_scans > 0 else 0)
    
    # Format recent activity
    recent_activity = []
    for scan in scans[:5]:  # Only get the 5 most recent scans
        recent_activity.append({
            'product_name': scan.product_name,
            'recyclable': scan.recyclable,
            'time': scan.scanned_at.strftime('%Y-%m-%d %H:%M')
        })
    
    return jsonify({
        'total_scans': total_scans,
        'recycling_impact': recycling_impact,
        'recent_activity': recent_activity
    })